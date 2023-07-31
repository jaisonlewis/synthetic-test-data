# synthetic-test-data
This generates synthetic test data with white circles, blue triangles and red squares.
The 256X256 image is divided into random quadrants 4 9 16 and then generates either a square, circle or a triangle in the quadrant. 
Initially, the objects were overlapping, so restricted their size to the max size of the quadrant
The program also uses the data to create a mask with white background and black outlines.
It then uses the data at hand to enter coordinates into a csv file... however, the data in the csv needs more work. 
