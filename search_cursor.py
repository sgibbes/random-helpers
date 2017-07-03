import arcpy

arcpy.env.workspace = 'c:/data/output.gdb'
fc = 'c:/data/base.gdb/roads'
fields = ['ROAD_TYPE', 'BUFFER_DISTANCE']

# Create update cursor for feature class 
with arcpy.da.UpdateCursor(fc, fields) as cursor:
    # Update the field used in Buffer so the distance is based on road 
    # type. Road type is either 1, 2, 3, or 4. Distance is in meters. 
    for row in cursor:
        # Update the BUFFER_DISTANCE field to be 100 times the 
        # ROAD_TYPE field.
        row[1] = row[0] * 100
        cursor.updateRow(row) 

