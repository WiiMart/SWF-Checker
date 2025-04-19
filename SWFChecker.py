import os
import zlib
import sys

print(f"SWF Version Checker v1.0\nPython {sys.version}")
os.system("title SWF Version Checker v1.0")
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

        file_attributes_index = obj.find(b'\x45')
        if file_attributes_index != -1:
            flag = obj[file_attributes_index + 2]
            isas3 = bool(flag & 0x08)
            asver = "3 (this game WILL NOT work on the Wii)" if isas3 else "1/2 (this version is compatible with the Wii!)"
        else:
            asver = "Unable to detect ActionScript version, please try again"

        return flashver, asver, obj
    except KeyboardInterrupt:
        print("Exiting...")
        exit()
    except Exception as e:
        print(f"Exception occurred!\n{e}")
        exit()

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

    return w, h

flashver, asver, SWFDAT = CheckSWF(swf)

if flashver is not None:
    w, h = GetStageWH(SWFDAT)
    print(f"SWF Dimensions: {w}x{h} pixels")

    if flashver > 8:
        print(f"Flash version: {flashver}, this version may NOT be compatible with the Wii.")
    else:
        print(f"Flash version: {flashver}, this version is compatible with the Wii.")
    
    print(f"ActionScript version: {asver}")

    if w > 700 and h > 500:
        print("WARNING: The given SWF might overlap/clip on the Wii.")
    else:
        print("The SWF should NOT overlap and/or clip on the Wii.")
