from schismpy.mesh.hgrid import Hgrid

hgridDir  = 'read_hgrid_sample.gr3'
hgrid_dict = Hgrid.open(hgridDir)

nobc = hgrid_dict['# of Open boundaries']
print(hgrid_dict['Node'])
#for no in range(nobc):
#    data = hgrid_dict['Obc'+str(no+1)]
#    print(data)
