import os
import platform
import zlib
from sys import platform, exit

platf = platform.system()
if platf == "Windows"
    os.system("title SWF Checker v2.3")
    os.system("cls")
else:
    os.system("clear")

print(f"SWF Version Checker v2.3\nPython {version}")

try:
    swf = input("SWF Filename: ").strip()
except KeyboardInterrupt:
    print("\nExiting...")
    exit()

def CheckSWF(swf):
    try:
        if not os.path.exists(swf):
            print("Error: File not found. Please check the filename and try again.")
            return None, None, None

        with open(swf, "rb") as f:
            obj = f.read()

        # decompress (CWS, zlib)
        if obj[:3] == b"CWS":
            print("SWF is compressed (zlib, CWS head), uncompressing...")
            obj = b"FWS" + obj[3:8] + zlib.decompress(obj[8:])

        flashver = obj[3]

        result_isas3 = False
        fileAttrIdx = obj.find(b'\x45')
        # looks for FileAttributes, (actionScript3: false/true)
        if fileAttrIdx != -1:
            flags_byte = obj[fileAttrIdx + 2]
            if flags_byte in [0x0, 0x1]:
                result_isas3 = False
            else:
                result_isas3 = (flags_byte & 0x08) != 0

        # fallback method (looks for doabc (as3 only))
        else:
            doabc_IDX = obj.find(b'\x52')
            if doabc_IDX != -1:
                doabc_len = int.from_bytes(obj[doabc_IDX+1:doabc_IDX+4], "little")
                result_isas3 = (doabc_len > 10)
            else:
                result_isas3 = False

        # looks for doaction (as2/1 only)
        doact_idx = obj.find(b'\x0C')
        if doact_idx != -1 and not result_isas3:
            result_isas3 = False

        if flashver < 9:
            if result_isas3:
                isas3 = True
            else:
                isas3 = False
        else:
            isas3 = result_isas3

        asver = "ActionScript 3.0 (incompatible)" if isas3 else "ActionScript 1.0/2.0 (compatible)"
        return flashver, asver, obj

    except KeyboardInterrupt:
        print("\nExiting...")
        exit()
    except Exception as e:
        print(f"exception occurred!\n{e}")
        return None, None, None

def GetStageWH(obj):
    rectS = 8
    nbits = (obj[rectS] >> 3) & 0x1F
    bOffset = rectS * 8 + 5

    def ReadBit(offset, bits_Num):
        ByteOffs = offset // 8
        BShift = offset % 8
        val = int.from_bytes(obj[ByteOffs:ByteOffs + 4], "big")
        return (val >> (32 - bits_Num - BShift)) & ((1 << bits_Num) - 1)

    XMin = ReadBit(bOffset, nbits)
    XMax = ReadBit(bOffset + nbits, nbits)
    YMin = ReadBit(bOffset + 2 * nbits, nbits)
    YMax = ReadBit(bOffset + 3 * nbits, nbits)

    w = round((XMax - XMin) / 20, 2)
    h = round((YMax - YMin) / 20, 2)
    return w, h # w=width, h=height, px

flashver, asver, SWFDAT = CheckSWF(swf)

if flashver is not None:
    w, h = GetStageWH(SWFDAT)
    print(f"SWF Dimensions: {w}x{h} pixels")
    if flashver > 8:
        print(f"Flash version: {flashver}, this version MAY NOT be compatible with the Wii.")
    else:
        print(f"Flash version: {flashver}, this version is compatible with the Wii.")
    print(f"ActionScript version: {asver}")
    if w > 700 and h > 500:
        print("WARNING: The given SWF might overlap/clip on the Wii.")
    else:
        print("The SWF should NOT overlap and/or clip on the Wii.")

    if platf == "Windows":
        os.system("pause")
        exit()
    else:
        os.system("/bin/bash -c 'read -s -n 1 -p \"Press any key to exit.\"'")
        exit()
