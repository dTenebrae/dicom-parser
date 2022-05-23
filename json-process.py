import sys, json

def unpack_json(json_data):
    return {
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
            "Image_size": (json_data["00280010"]["Value"][0], json_data["00280011"]["Value"][0]),
            "filename": json_data["00080018"]["Value"][0]
            }

def main():
    json_data = json.load(sys.stdin)
    print(json.dumps(unpack_json(json_data)))

if __name__ == "__main__":
    main()
