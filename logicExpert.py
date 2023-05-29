from typing import ClassVar

from connection_data import area_doors_unpackable
from door_logic import canOpen
from item_data import items_unpackable
from loadout import Loadout
from logicInterface import AreaLogicType, LocationLogicType, LogicInterface
from logic_shortcut import LogicShortcut

# TODO: There are a bunch of places where where Expert logic needed energy tanks even if they had Varia suit.
# Need to make sure everything is right in those places.
# (They will probably work right when they're combined like this,
#  but they wouldn't have worked right when casual was separated from expert.)

# TODO: There are also a bunch of places where casual used icePod, where expert only used Ice. Is that right?

(
    CraterR, SunkenNestL, RuinedConcourseBL, RuinedConcourseTR, CausewayR,
    SporeFieldTR, SporeFieldBR, OceanShoreR, EleToTurbidPassageR, PileAnchorL,
    ExcavationSiteL, WestCorridorR, FoyerR, ConstructionSiteL, AlluringCenoteR,
    FieldAccessL, TransferStationR, CellarR, SubbasementFissureL,
    WestTerminalAccessL, MezzanineConcourseL, VulnarCanyonL, CanyonPassageR,
    ElevatorToCondenserL, LoadingDockSecurityAreaL, ElevatorToWellspringL,
    NorakBrookL, NorakPerimeterTR, NorakPerimeterBL, VulnarDepthsElevatorEL,
    VulnarDepthsElevatorER, HiveBurrowL, SequesteredInfernoL,
    CollapsedPassageR, MagmaPumpL, ReservoirMaintenanceTunnelR, IntakePumpR,
    ThermalReservoir1R, GeneratorAccessTunnelL, ElevatorToMagmaLakeR,
    MagmaPumpAccessR, FieryGalleryL, RagingPitL, HollowChamberR, PlacidPoolR,
    SporousNookL, RockyRidgeTrailL, TramToSuziIslandR
) = area_doors_unpackable

(
    Missile, Super, PowerBomb, Morph, Springball, Bombs, HiJump,
    GravitySuit, Varia, Wave, SpeedBooster, Spazer, Ice, Grapple,
    Plasma, Screw, Charge, SpaceJump, Energy, Reserve, Xray
) = items_unpackable

pinkDoor = LogicShortcut(lambda loadout: (
    (Missile in loadout) or
    (Super in loadout)
))
canUseBombs = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    ((Bombs in loadout) or (PowerBomb in loadout))
))
canUsePB = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (PowerBomb in loadout)
))

BT = LogicShortcut(lambda loadout: (
    (Morph in loadout) and
    (Bombs in loadout) and
    (Missile in loadout)
))
goingLeft = LogicShortcut(lambda loadout: (
    (
        (Morph in loadout) and
        (
            ((canUsePB in loadout) and (Super in loadout)) or
            (SpeedBooster in loadout)
            )
        )
))
WS = LogicShortcut(lambda loadout: (
    (BT in loadout) and
    (canUsePB in loadout)
))
greenBrin = LogicShortcut(lambda loadout: (
    (BT in loadout) and
    (canUsePB in loadout) and
    (Wave in loadout) and
    (Super in loadout)
))
morphMaze = LogicShortcut(lambda loadout: (
    (canUseBombs in loadout) or
    (
        (Morph in loadout) and
        (Springball in loadout)
        )
))
maridia = LogicShortcut(lambda loadout: (
    (BT in loadout) and
    (Super in loadout) and
    (SpeedBooster in loadout) and
    (
        (greenBrin in loadout) or
        (
            (canUsePB in loadout) and
            (GravitySuit in loadout)
            )
        )
))
norfair = LogicShortcut(lambda loadout: (
    (BT in loadout) and
    (Super in loadout) and
    (Varia in loadout)
))
lowerNorfair = LogicShortcut(lambda loadout: (
    (maridia in loadout) and
    (Varia in loadout) and
    (Charge in loadout) and
    ((GravitySuit in loadout) or
     (HiJump in loadout))
))
tourian = LogicShortcut(lambda loadout: (
    (lowerNorfair in loadout) and
    (GravitySuit in loadout) and
    (Wave in loadout)
))

area_logic: AreaLogicType = {
    "Early": {
        # using SunkenNestL as the hub for this area, so we don't need a path from every door to every other door
        # just need at least a path with sunken nest to and from every other door in the area
        ("CraterR", "SunkenNestL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "CraterR"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseBL"): lambda loadout: (
            True
        ),
        ("SunkenNestL", "RuinedConcourseTR"): lambda loadout: (
            True
            # TODO: Expert needs energy and casual doesn't? And Casual can do it with supers, but expert can't?
        ),   
    },
}


location_logic: LocationLogicType = {
"Crater Reserve Tank": lambda loadout: (
                (canUseBombs in loadout)
),
"Parlor Chozo Missile": lambda loadout: (
    (Morph in loadout)
),
"Parlor Ceiling Missile": lambda loadout: (
    True
),
"Parlor Right Missile": lambda loadout: (
    (Morph in loadout)
),
"Pre Phantoon Wall": lambda loadout: (
    (BT in loadout)
),
"WS Pancake Entry": lambda loadout: (
    (WS in loadout)
),
"Crateria Cage": lambda loadout: (
    (goingLeft in loadout) and
    (
        (SpaceJump in loadout) or
        (GravitySuit in loadout)
        )
     
),
"Gauntlet Missile": lambda loadout: (
    (canUsePB in loadout) and
    (Super in loadout)
),
"Gauntlet Power Bomb": lambda loadout: (
    (canUseBombs in loadout) and
    (Super in loadout)
),
"Mushroom Deep Wall Missile": lambda loadout: (
    (BT in loadout)
),
"Mushroom Wall Energy Tank": lambda loadout: (
    (BT in loadout)
),
"Mushroom Hidden": lambda loadout: (
    (BT in loadout)
),
"Bombs": lambda loadout: (
    (pinkDoor in loadout)
),
"Morph Ball": lambda loadout: (
    True
),
"Above Mushroom Missile": lambda loadout: (
    (BT in loadout)
),
"Gauntlet Energy Tank": lambda loadout: (
    (canUsePB in loadout) and
    (Super in loadout)
),
"Gauntlet Super Missile": lambda loadout: (
    (canUsePB in loadout) and
    (Super in loadout)
    
),
"Brinstar Floor Missile": lambda loadout: (
    (BT in loadout)
),
"Brinstar Ceiling E": lambda loadout: (
    (BT in loadout)
),
"Triple Missile Middle": lambda loadout: (
    (greenBrin in loadout)
),
"Triple Missile Right": lambda loadout: (
    (greenBrin in loadout)
),
"Triple Missile Left": lambda loadout: (
    (greenBrin in loadout)
),
"Grapple Chozo Missile": lambda loadout: (
    (goingLeft in loadout) and
    ((GravitySuit in loadout) or (SpaceJump in loadout)) and
    (Grapple in loadout) and
    (morphMaze in loadout)
),
"Grapple Maze Super": lambda loadout: (
    (goingLeft in loadout) and
    ((GravitySuit in loadout) or (SpaceJump in loadout)) and
    (Grapple in loadout) and
    (morphMaze in loadout)
),
"Springball": lambda loadout: (
    (goingLeft in loadout) and
    ((GravitySuit in loadout) or (SpaceJump in loadout)) and
    (Grapple in loadout) and
    (morphMaze in loadout)
),
"Kihunter Speed Hallway Floor": lambda loadout: (
    (greenBrin in loadout)
),
"Final Escape PB": lambda loadout: (
    (goingLeft in loadout) and
    ((GravitySuit in loadout) or (SpaceJump in loadout)) and
    (canUsePB in loadout)
),
"Green Hoppers Flower Missile": lambda loadout: (
    (greenBrin in loadout)
),
"Charge Beam": lambda loadout: (
    (BT in loadout)
),
"Green Shaft Missile": lambda loadout: (
    (greenBrin in loadout)
),
"Brinstar Floor PB": lambda loadout: (
    (BT in loadout) and
    (Super in loadout)
),
"Alpha Super": lambda loadout: (
    (BT in loadout) and
    (Super in loadout)
),
"Grapple Beam": lambda loadout: (
    (goingLeft in loadout) and
    ((GravitySuit in loadout) or (SpaceJump in loadout)) and
    (Grapple in loadout) and
    (morphMaze in loadout)
),
"Green Flower E": lambda loadout: (
    (greenBrin in loadout)
),
"Spazer Energy": lambda loadout: (
    (greenBrin in loadout)
),
"Purple Warehouse Ceiling": lambda loadout: (
    (maridia in loadout)
),
"Purple Warehouse Floor": lambda loadout: (
    (maridia in loadout)
),
"Ice Hidden Middle": lambda loadout: (
    (maridia in loadout)
),
"Ice Beam": lambda loadout: (
    (maridia in loadout)
),
"Ice Hidden Wall": lambda loadout: (
    (maridia in loadout)
),
"Kraid Tide Chozo": lambda loadout: (
    (BT in loadout) and
    (Super in loadout)
),
"Kraid Tide Underwater": lambda loadout: (
    (BT in loadout) and
    (Super in loadout)
),
"Escape Chozo Missile": lambda loadout: (
    (goingLeft in loadout) and
    ((GravitySuit in loadout) or (SpaceJump in loadout)) and
    (Ice in loadout) and
    (Xray in loadout)
),
"Escape Purple Tunnel": lambda loadout: (
    (goingLeft in loadout) and
    ((GravitySuit in loadout) or (SpaceJump in loadout))
),
"Spazer": lambda loadout: (
    (greenBrin in loadout)
),
"Green Kihunter Nook": lambda loadout: (
    (greenBrin in loadout)
),
"Baby Kraid PB": lambda loadout: (
    (BT in loadout) and
    (Super in loadout)
),
"HiJump": lambda loadout: (
    (BT in loadout) and
    (Super in loadout)
),
"Norfair Wall Super": lambda loadout: (
    (norfair in loadout)
),
"Croc Power Bomb": lambda loadout: (
    (norfair in loadout) and
    (SpeedBooster in loadout)
),
"Norfair Entrance Wall": lambda loadout: (
    (BT in loadout) and
    (Super in loadout)
),
"Norfair Entrance E": lambda loadout: (
    (BT in loadout) and
    (Super in loadout)
),
"Purple Bubble Farm Secret": lambda loadout: (
    (norfair in loadout)
),
"Varia Suit": lambda loadout: (
    (norfair in loadout)
),
"Speed Exit Missile": lambda loadout: (
    (norfair in loadout)
),
"Puyo Pool": lambda loadout: (
    (norfair in loadout)
),
"Croc Mist Wall": lambda loadout: (
    (norfair in loadout) and
    (SpeedBooster in loadout)
),
"Speed Hallway Pit": lambda loadout: (
    (norfair in loadout)
),
"Speed Booster": lambda loadout: (
    (norfair in loadout)
),
"LN Escape Kago Reserve": lambda loadout: (
    (lowerNorfair in loadout)
),
"Spazer Reserve": lambda loadout: (
    (greenBrin in loadout)
),
"Spazer Bug Blue Wall": lambda loadout: (
    (greenBrin in loadout)
),
"Spazer Chozo Missile": lambda loadout: (
    (greenBrin in loadout)
),
"Acid Floor": lambda loadout: (
    (lowerNorfair in loadout) and
    (GravitySuit in loadout)
),
"Acid Chozo": lambda loadout: (
    (lowerNorfair in loadout) and
    (GravitySuit in loadout)
),
"GT Energy": lambda loadout: (
    (lowerNorfair in loadout) and
    (GravitySuit in loadout)
),
"Ridley Floor Missile": lambda loadout: (
    (lowerNorfair in loadout)
),
"Space Floor": lambda loadout: (
    (lowerNorfair in loadout)
),
"LN Pirate Wall Super": lambda loadout: (
    (lowerNorfair in loadout)
),
"Space Jump Missile": lambda loadout: (
    (lowerNorfair in loadout) and
    (GravitySuit in loadout)
),
"Space Jump": lambda loadout: (
    (lowerNorfair in loadout) and
    (GravitySuit in loadout)
),
"LN Speed Floor": lambda loadout: (
    (lowerNorfair in loadout) and
    (SpeedBooster in loadout)
),
"Ridley Reward": lambda loadout: (
    (lowerNorfair in loadout)
),
"LN Chozo Chain E": lambda loadout: (
    (lowerNorfair in loadout)
),
"Phantoon Unpowered Missile": lambda loadout: (
    (WS in loadout)
),
"WS Floor PB": lambda loadout: (
    (WS in loadout)
),
"WS Ceiling E": lambda loadout: (
    (WS in loadout)
),
"Wave Beam": lambda loadout: (
    (WS in loadout)
),
"Gravity Suit": lambda loadout: (
    (WS in loadout)
),
"Tube Spark": lambda loadout: (
    (maridia in loadout) and
    (SpeedBooster in loadout)
),
"Tide-Tube Ceiling": lambda loadout: (
    (BT in loadout) and
    (Super in loadout)
),
"Lower Maridia Chozo": lambda loadout: (
    (maridia in loadout) and
    ((GravitySuit in loadout) or
     (HiJump in loadout))
),
"Mama Chozo": lambda loadout: (
    (maridia in loadout) and
    (GravitySuit in loadout)
),
"Mama Floor": lambda loadout: (
    (maridia in loadout) and
    (GravitySuit in loadout)
),
"Green Maridia E": lambda loadout: (
    (maridia in loadout)
),
"Serpent Trench Missile": lambda loadout: (
    (maridia in loadout)
),
"Screw Attack": lambda loadout: (
    (maridia in loadout) and
    ((GravitySuit in loadout) or
     (HiJump in loadout))
),
"G4 Maridia Sand": lambda loadout: (
    (tourian in loadout)
),
"Sand Bug Farm": lambda loadout: (
    (maridia in loadout) and
    (
        (GravitySuit in loadout) or
        (
            (Ice in loadout) and
            (HiJump in loadout)
            )
        )
),
"Draygon Ceiling Super": lambda loadout: (
    (maridia in loadout) and
    (GravitySuit in loadout)
),
"Xray": lambda loadout: (
    (maridia in loadout) and
    (GravitySuit in loadout) and
    (SpeedBooster in loadout)
),
"Mochtroids Chozo": lambda loadout: (
    (maridia in loadout) and
    ((GravitySuit in loadout) or
     (HiJump in loadout))
),
"Mochtroids Wall": lambda loadout: (
    (maridia in loadout) and
    ((GravitySuit in loadout) or
     (HiJump in loadout))
),
"Plasma Beam": lambda loadout: (
    (maridia in loadout) and
    (GravitySuit in loadout)
),
"Upper Maridia Chozo": lambda loadout: (
    (maridia in loadout) and
    ((GravitySuit in loadout) or
     (HiJump in loadout))
),
"Metroids Missile": lambda loadout: (
    (tourian in loadout)
),
"Baby Sand E": lambda loadout: (
    (tourian in loadout)
),
}


class Expert(LogicInterface):
    area_logic: ClassVar[AreaLogicType] = area_logic
    location_logic: ClassVar[LocationLogicType] = location_logic

    @staticmethod
    def can_fall_from_spaceport(loadout: Loadout) -> bool:
        return True
