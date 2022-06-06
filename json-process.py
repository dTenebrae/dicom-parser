import sys, json

def extract_coordinates(json_data):
    """
    https://stackoverflow.com/questions/10241062/how-to-draw-scout-reference-lines-in-dicom

    Example:

        Group,Elem  VR Value                           Name of the tag
    ---------------------------------------------------------------------
    (0020,0032) DS [-249.51172\-417.51172\-821]  # ImagePositionPatient
                    X0         Y0         Z0

    (0020,0037) DS [1\0\0\0\1\0]                 # ImageOrientationPatient
                    A B C D E F

    scr = refers to the soruce image, i.e. the MR/CT slice
    dst = refers to the destination image, i.e. the scout

    pos_x, pos_y, pos_z = the X0, Y0, Z0 above
    row_dircos_x, row_dircos_y, row_dircos_z = the A, B, C above
    col_dircos_x, col_dircos_y, col_dircos_z = the D, E, F above
    """

    pos_x, pos_y, pos_z = json_data["00200032"]["Value"]
    img_orientation = json_data["00200037"]["Value"]
    row_dircos_x, row_dircos_y, row_dircos_z = img_orientation[:3]
    col_dircos_x, col_dircos_y, col_dircos_z = img_orientation[3:]

    return {
        "pos_x": pos_x,
        "pos_y": pos_y,
        "pos_z": pos_z,
        "row_dircos_x": row_dircos_x,
        "row_dircos_y": row_dircos_y,
        "row_dircos_z": row_dircos_z,
        "col_dircos_x": col_dircos_x,
        "col_dircos_y": col_dircos_y,
        "col_dircos_z": col_dircos_z
    }

def unpack_json(json_data):
    coord = extract_coordinates(json_data)
    return {
            "UID": json_data["00080018"]["Value"][0],
            "Name": json_data["00100010"]["Value"][0]['Alphabetic'],
            "Sex": json_data["00100040"]["Value"][0],
            "Birth_date": json_data["00100030"]["Value"][0],
            "Age": json_data["00101010"]["Value"][0],
            "Weight": json_data["00101030"]["Value"][0],
            "Procedure_date": json_data["00080020"]["Value"][0],
            "Region": json_data["00081030"]["Value"][0],
            "Sequence_name": json_data["0008103E"]["Value"][0],
            "Sequence_dim": json_data["00180023"]["Value"][0],
            "Sequence_base": json_data["00180024"]["Value"][0],
            "Slice_thickness": json_data["00180050"]["Value"][0],
            "Coil": json_data["00181250"]["Value"][0],
            "Matrix": json_data["00181310"]["Value"],
            "Image_size": (json_data["00280010"]["Value"][0],
                json_data["00280011"]["Value"][0]),
            "pos_x": coord["pos_x"],
            "pos_y": coord["pos_y"],
            "pos_z": coord["pos_z"],
            "row_dircos_x": coord["row_dircos_x"],
            "row_dircos_y": coord["row_dircos_y"],
            "row_dircos_z": coord["row_dircos_z"],
            "col_dircos_x": coord["col_dircos_x"],
            "col_dircos_y": coord["col_dircos_y"],
            "col_dircos_z": coord["col_dircos_z"]
            }

def main():
    json_data = json.load(sys.stdin)
    print(json.dumps(unpack_json(json_data)))

if __name__ == "__main__":
    main()
