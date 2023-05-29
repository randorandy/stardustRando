import random
import sys
from typing import Literal, Optional, Type
import argparse

from connection_data import SunkenNestL, VanillaAreas
from fillInterface import FillAlgorithm
from game import Game
from item_data import Item, Items, items_unpackable
from loadout import Loadout
from location_data import Location, pullCSV, spacePortLocs
from logicExpert import Expert
import logic_updater
import fillAssumed
import areaRando
from romWriter import RomWriter
from solver import solve


def plmidFromHiddenness(itemArray, hiddenness) -> bytes:
    if hiddenness == "open":
        plmid = itemArray[1]
    elif hiddenness == "chozo":
        plmid = itemArray[2]
    else:
        plmid = itemArray[3]
    return plmid

def write_location(romWriter: RomWriter, location: Location) -> None:
    """
    provide a location with an ['item'] value, such as Missile, Super, etc
    write all rom locations associated with the item location
    """
    item = location["item"]
    assert item, f"{location['fullitemname']} didn't get an item"
    # TODO: support locations with no items?
    plmid = plmidFromHiddenness(item, location['hiddenness'])
    for address in location['locids']:
        romWriter.writeItem(address, plmid, item[4])
    for address in location['alternateroomlocids']:
        if location['alternateroomdifferenthiddenness'] == "":
            # most of the alt rooms go here, having the same item hiddenness
            # as the corresponding "pre-item-move" item had
            plmid_altroom = plmid
        else:
            plmid_altroom = plmidFromHiddenness(item, location['alternateroomdifferenthiddenness'])
        romWriter.writeItem(address, plmid_altroom, item[4])


fillers: dict[str, Type[FillAlgorithm]] = {
    "AF": fillAssumed.FillAssumed,
}


# main program
def Main(argv: list[str], romWriter: Optional[RomWriter] = None) -> None:
    

    logicChoice = "E"
    fillChoice = "D"
    areaA = ""
    

    # hudFlicker=""
    # while hudFlicker != "Y" and hudFlicker != "N" :
    #     hudFlicker= input("Enter Y to patch HUD flicker on emulator, or N to decline:")
    #     hudFlicker = hudFlicker.title()
    seeeed = random.randint(1000000, 9999999)
    random.seed(seeeed)
    rom_name = f"Stardust{seeeed}.sfc"
    rom1_path = f"roms/{rom_name}"
    rom_clean_path = "roms/Stardust.sfc"
    # you must include Eris 2012 in your roms folder with this name^

    csvdict = pullCSV()
    locArray = list(csvdict.values())

    if romWriter is None :
        romWriter = RomWriter.fromFilePaths(
            origRomPath=rom_clean_path, newRomPath=rom1_path)
    else :
        # remove .sfc extension and dirs
        romWriter.setBaseFilename(rom1_path[:-4].split("/")[-1])

    spoilerSave = ""
    seedComplete = False
    randomizeAttempts = 0
    game = Game(Expert if logicChoice == "E" else Casual,
                csvdict,
                areaA == "A",
                VanillaAreas())
    while not seedComplete :
        if game.area_rando:  # area rando
            game.connections = areaRando.RandomizeAreas()
            # print(Connections) #test
        randomizeAttempts += 1
        if randomizeAttempts > 1000 :
            print("Giving up after 1000 attempts. Help?")
            break
        print("Starting randomization attempt:", randomizeAttempts)
        spoilerSave = ""
        spoilerSave += f"Starting randomization attempt: {randomizeAttempts}\n"
        # now start randomizing
        if fillChoice == "D":
            seedComplete, spoilerSave = assumed_fill(game, spoilerSave)
        else:
            seedComplete, spoilerSave = forward_fill(game, fillChoice, spoilerSave)

    # add area transitions to spoiler
    if game.area_rando:
        for item in game.connections:
            spoilerSave += f"{item[0][2]} {item[0][3]} << >> {item[1][2]} {item[1][3]}\n"

    _got_all, solve_lines, _locs = solve(game)

    if game.area_rando:
        areaRando.write_area_doors(game.connections, romWriter)
    # write all items into their locations
    for loc in locArray:
        write_location(romWriter, loc)

    # NOTE THESE ADDRESSES ARE INCREASED BY 0x200 for Stardust
    
    # Skip Ceres
    #romWriter.writeBytes(0x16ebb, b"\x05")
    # Morph Ball Fix
    romWriter.writeBytes(0x26ace, b"\x04")
    romWriter.writeBytes(0x27002, b"\x04")

    # Suit animation skip patch
    romWriter.writeBytes(0x20917, b"\xea\xea\xea\xea")
    
    # Remove gravity suit heat protection #test
    romWriter.writeBytes(0x6e57d, b"\x01")
    romWriter.writeBytes(0x86bdd, b"\x01")
    
    # Change hidden mushroom room to only require morph
    romWriter.writeBytes(0x79967, b"\x40")
    
    romWriter.finalizeRom()
    print("Done!")
    print(f"Filename is {rom_name}")
    with open(f"spoilers/{rom_name}.spoiler.txt", "w") as spoiler_file:
        spoiler_file.write(f"RNG Seed: {seeeed}\n\n")
        spoiler_file.write("\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n")
        spoiler_file.write(spoilerSave)
        spoiler_file.write('\n\n')
        for solve_line in solve_lines:
            spoiler_file.write(solve_line + '\n')
    print(f"Spoiler file is spoilers/{rom_name}.spoiler.txt")


def assumed_fill(game: Game, spoilerSave: str) -> tuple[bool, str]:
    for loc in game.all_locations.values():
        loc["item"] = None
    dummy_locations: list[Location] = []
    loadout = Loadout(game)
    fill_algorithm = fillAssumed.FillAssumed(game.connections)
    n_items_to_place = fill_algorithm.count_items_remaining()
    assert n_items_to_place <= len(game.all_locations), \
        f"{n_items_to_place} items to put in {len(game.all_locations)} locations"
    print(f"{fill_algorithm.count_items_remaining()} items to place")
    while fill_algorithm.count_items_remaining():
        placePair = fill_algorithm.choose_placement(dummy_locations, loadout)
        if placePair is None:
            message = ('Item placement was not successful in assumed. '
                       f'{fill_algorithm.count_items_remaining()} items remaining.')
            print(message)
            spoilerSave += f'{message}\n'
            break
        placeLocation, placeItem = placePair
        placeLocation["item"] = placeItem
        spoilerSave += f"{placeLocation['fullitemname']} - - - {placeItem[0]}\n"

        if fill_algorithm.count_items_remaining() == 0:
            # Normally, assumed fill will always make a valid playthrough,
            # but dropping from spaceport can mess that up,
            # so it needs to be checked again.
            #completable, _, _ = solve(game)
            completable = True
            if completable:
                print("Item placements successful.")
                spoilerSave += "Item placements successful.\n"
            return completable, spoilerSave

    return False, spoilerSave


def forward_fill(game: Game,
                 fillChoice: Literal["M", "S", "MM"],
                 spoilerSave: str) -> tuple[bool, str]:
    unusedLocations : list[Location] = []
    unusedLocations.extend(game.all_locations.values())
    availableLocations: list[Location] = []
    # visitedLocations = []
    loadout = Loadout(game)
    loadout.append(SunkenNestL)  # starting area
    # use appropriate fill algorithm for initializing item lists
    fill_algorithm = fillers[fillChoice](game.connections)
    while len(unusedLocations) != 0 or len(availableLocations) != 0:
        # print("loadout contains:")
        # print(loadout)
        # for a in loadout:
        #     print("-",a[0])
        # update logic by updating unusedLocations
        # using helper function, modular for more logic options later
        # unusedLocations[i]['inlogic'] holds the True or False for logic
        logic_updater.updateAreaLogic(loadout)
        logic_updater.updateLogic(unusedLocations, loadout)

        # update unusedLocations and availableLocations
        for i in reversed(range(len(unusedLocations))):  # iterate in reverse so we can remove freely
            if unusedLocations[i]['inlogic'] is True:
                # print("Found available location at",unusedLocations[i]['fullitemname'])
                availableLocations.append(unusedLocations[i])
                unusedLocations.pop(i)
        # print("Available locations sits at:",len(availableLocations))
        # for al in availableLocations :
        #     print(al[0])
        # print("Unused locations sits at size:",len(unusedLocations))
        # print("unusedLocations:")
        # for u in unusedLocations :
        #     print(u['fullitemname'])

        if availableLocations == [] and unusedLocations != [] :
            print(f'Item placement was not successful. {len(unusedLocations)} locations remaining.')
            spoilerSave += f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
            # for i in loadout:
            #     print(i[0])
            # for u in unusedLocations :
            #     print("--",u['fullitemname'])

            break

        placePair = fill_algorithm.choose_placement(availableLocations, loadout)
        if placePair is None:
            print(f'Item placement was not successful due to majors. {len(unusedLocations)} locations remaining.')
            spoilerSave += f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
            break
        # it returns your location and item, which are handled here
        placeLocation, placeItem = placePair
        if (placeLocation in unusedLocations) :
            unusedLocations.remove(placeLocation)
        placeLocation["item"] = placeItem
        availableLocations.remove(placeLocation)
        fill_algorithm.remove_from_pool(placeItem)
        loadout.append(placeItem)
        if not ((placeLocation['fullitemname'] in spacePortLocs) or (Items.spaceDrop in loadout)):
            loadout.append(Items.spaceDrop)
        spoilerSave += f"{placeLocation['fullitemname']} - - - {placeItem[0]}\n"
        # print(placeLocation['fullitemname']+placeItem[0])

        if availableLocations == [] and unusedLocations == [] :
            print("Item placements successful.")
            spoilerSave += "Item placements successful.\n"
            return True, spoilerSave
    return False, spoilerSave


if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    Main(sys.argv)
    t1 = time.perf_counter()
    print(f"time taken: {t1 - t0}")
