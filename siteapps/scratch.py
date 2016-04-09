import cloudconvert # pip install cloudconvert

api = cloudconvert.Api('HKi3ooM6JI_caLFxb90B5lYONnKmoGjGNZ8R3Ozx22XB9pJJDzk1wx9fBgJEDqu-s_gmwWc1R31h_YPABQOZjw')

process = api.convert({
    "input": "upload",
    "email": "true",
    "inputformat": "pdf",
    "outputformat": "html",
    "file": open('../CisnerosSandra-Eleven.pdf', 'rb')
})
process.wait()
process.download('../templates/')