#!/usr/bin/env python3

"""
scrap mesh data from density_render.ply
write another box.ply

This is just the bounding (crop) box for the cloud density data....
"""

import numpy


header = """\
ply
format binary_little_endian 1.0
comment VCGLIB generated
element vertex 8
property float x
property float y
property float z
element face 12
property list uchar int vertex_indices
end_header
"""

data = b'R\xb8\xfe?\xcd\xcc\xcc=\xcd\xcc\xcc=R\xb8\xfe?\xcd\xcc\xcc=q=J?\xcd\xcc\xcc=\xcd\xcc\xcc=q=J?\xcd\xcc\xcc=\xcd\xcc\xcc=\xcd\xcc\xcc=R\xb8\xfe?R\xb8\xfe?\xcd\xcc\xcc=R\xb8\xfe?R\xb8\xfe?q=J?\xcd\xcc\xcc=R\xb8\xfe?q=J?\xcd\xcc\xcc=R\xb8\xfe?\xcd\xcc\xcc=\x03\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x03\x04\x00\x00\x00\x07\x00\x00\x00\x06\x00\x00\x00\x03\x04\x00\x00\x00\x06\x00\x00\x00\x05\x00\x00\x00\x03\x00\x00\x00\x00\x04\x00\x00\x00\x05\x00\x00\x00\x03\x00\x00\x00\x00\x05\x00\x00\x00\x01\x00\x00\x00\x03\x01\x00\x00\x00\x05\x00\x00\x00\x06\x00\x00\x00\x03\x01\x00\x00\x00\x06\x00\x00\x00\x02\x00\x00\x00\x03\x02\x00\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x03\x02\x00\x00\x00\x07\x00\x00\x00\x03\x00\x00\x00\x03\x04\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x03\x04\x00\x00\x00\x03\x00\x00\x00\x07\x00\x00\x00' 

#print(data)

# 8*(4 + 4 + 4) + 12*(1 + 4 + 4 + 4)

verts_s = data[:8*(4 + 4 + 4)]
faces_s = data[8*(4 + 4 + 4):]

verts = numpy.fromstring(verts_s, dtype=numpy.float32)
verts.shape = (8,3)
#print(verts)
"""
[[ 1.99000001  0.1         0.1       ]
 [ 1.99000001  0.1         0.79000002]
 [ 0.1         0.1         0.79000002]
 [ 0.1         0.1         0.1       ]
 [ 1.99000001  1.99000001  0.1       ]
 [ 1.99000001  1.99000001  0.79000002]
 [ 0.1         1.99000001  0.79000002]
 [ 0.1         1.99000001  0.1       ]]
"""


faces = numpy.fromstring(faces_s, dtype=numpy.uint8)
faces.shape = (12, 1+4+4+4)
#print(faces)
"""
[[3 0 0 0 0 1 0 0 0 2 0 0 0]
 [3 0 0 0 0 2 0 0 0 3 0 0 0]
 [3 4 0 0 0 7 0 0 0 6 0 0 0]
 [3 4 0 0 0 6 0 0 0 5 0 0 0]
 [3 0 0 0 0 4 0 0 0 5 0 0 0]
 [3 0 0 0 0 5 0 0 0 1 0 0 0]
 [3 1 0 0 0 5 0 0 0 6 0 0 0]
 [3 1 0 0 0 6 0 0 0 2 0 0 0]
 [3 2 0 0 0 6 0 0 0 7 0 0 0]
 [3 2 0 0 0 7 0 0 0 3 0 0 0]
 [3 4 0 0 0 0 0 0 0 3 0 0 0]
 [3 4 0 0 0 3 0 0 0 7 0 0 0]]
"""

output = bytearray(data)
print(output)

R =  2.1
V = -0.1
verts = numpy.array(
[[ R,   V, V ],
 [ R,   V, R   ],
 [ V, V, R   ],
 [ V, V, V ],
 [ R,   R,   V ],
 [ R,   R,   R   ],
 [ V, R,   R   ],
 [ V, R,   V ]], dtype=numpy.float32)
#verts[:, 0] *= 3.5

verts = verts.tostring()
assert len(verts) == len(verts_s)
print(verts)
output[:len(verts)] = verts

print(output)

#print(b''.join(bytes(i) for i in output))


f = open("box.ply", "wb")
f.write(header.encode())
f.write(output)
f.close()


