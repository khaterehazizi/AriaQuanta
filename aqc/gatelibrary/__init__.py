
#------------------------------------------------------------------------------------
from .gatesingle import (
    GateSingleQubit,
    I,
    GlobalPhase,
    X,
    Y,
    Z,
    S,
    Xsqrt,
    H,
    P,
    T,
    RX,
    RY,
    RZ,
    Rot,
)

#------------------------------------------------------------------------------------
from .gatedouble import (
    GateDoubleQubit,
    SWAP,
    ISWAP,
    SWAPsqrt,
    SWAPalpha,
    RXX,
    RYY,
    RZZ,
    RXY,
    Barenco,
    Berkeley,
    Canonical,
    Givens,
    Magic,
)

#------------------------------------------------------------------------------------
from .arxived_gatetriple import (
    GateTripleQubit,
    CCXold,
    CSWAPold,
)

#------------------------------------------------------------------------------------
from .gatecustom import (
    GateCustom,
    Custom,
)

#------------------------------------------------------------------------------------
from .gatecontrol import (
    GateControl,
    CU,
    CX,
    CZ,
    CP,
    CS,
    CSX,   
    CSWAP,
    CCX,
)

#------------------------------------------------------------------------------------
from .gatecontroln import (
    CNZ
)