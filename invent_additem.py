import json
f=open('plist.json','r')
r=f.read()
f.close()
products=json.loads(r)
item_count=int(input('Enter number of items to enter:'))
max_item=len(products)+item_count

while len(products)<max_item:
    id=str(1000+len(products)+1)
    name=input('Enter product name:')
    price=int(input('Enter price:'))
    qty=int(input('Enter qty:'))
    expiry=input('Enter expiry:')
    products.update({id:{'name':name,'price':price,'qty':qty,'expiry':expiry}})

r=json.dumps(products)
f=open('plist.json','w')
f.write(r)
f.close()