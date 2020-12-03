import csv
import json
# import time

import requests

csv_file = open('productDetails_Bullet.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(
    ['SKU', 'productName', 'description', 'category', 'subcategory', 'pricelevel1', 'colorName', 'packing', 'size',
     'image', 'otherImage', 'material', 'availableColours'])

URL = "http://niconceptws.com/api/NottageECommerceApi/GetCategorisation"

USERNAME = "your_user_name"
PASSWORD = "your_user_password"

headers = {
    "Content-Type": "application/json",
    "x-auth-token": "dXNlcm5hbWU6cGFzc3dvcmQ="

}
params = {
    "username": USERNAME,
    "password": PASSWORD,
    "nativeWorld": "Bullet"
}

response = requests.post(URL, headers=headers, data=json.dumps(params))
resp = response.json()

for categories in resp['data']['listOfCategory']:
    # print(categories['categoryName'])
    for subCategories in categories['listOfSubCategory']:
        # print(subCategories['subCategoryName'])
        # print('==================================')
        # print(subCategories)
        for productId in subCategories['listOfProducts']:
            # print(productId)
            getProductURL = "http://niconceptws.com/api/NottageECommerceApi/GetProduct"

            paramsTwo = {
                "username": USERNAME,
                "password": PASSWORD,
                "itemnumber": productId
            }
            # time.sleep(2)
            responseForProductInfo = requests.post(getProductURL, headers=headers, data=json.dumps(paramsTwo))
            getProductInfoJsonFormat = responseForProductInfo.json()
            # print(getProductInfoJsonFormat['data'])
            # print(getProductInfoJsonFormat['data']['listOfProducts'])
            for singleProduct in getProductInfoJsonFormat['data']['listOfProducts']:
                print(singleProduct)
                if singleProduct['size'] is not None:
                    if ';' in singleProduct['size']:
                        singleProduct['size'] = singleProduct['size'].replace(';', ',')
                    else:
                        singleProduct['size'] = singleProduct['size']
                else:
                    singleProduct['size'] = ''
                for colorDetails in singleProduct['colours']:
                    print(colorDetails['sku'])
                    csv_writer.writerow([
                    colorDetails['sku'], singleProduct['productName'], singleProduct['description'],
                    categories['categoryName'], subCategories['subCategoryName'], singleProduct['pricelevel1'],
                    colorDetails['colourName'], singleProduct['packing'], singleProduct['size'],
                    colorDetails['imageName'], singleProduct['otherImage'],
                    singleProduct['material'], singleProduct['availableColours']
                ])
print('Congrats! You have stolen all the data!')
csv_file.close()

