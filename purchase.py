import json
from datetime import datetime
from os import system,name,sys
try:
    from tabulate import tabulate
except:
    system('pip install tabulate')
    from tabulate import tabulate
def clear():
    if name == 'nt':
        _ = system('cls')   #for windows
    else:
        _ = system('clear') #for linux
clear()
def read(fname):
    f=open(f'{fname}.json','r')
    r=f.read()
    f.close()
    d=json.loads(r)
    return d
products=read('plist')
keys={i:1000+i for i in range(1,len(products)+1)}

def display_p():         #to display Content for customers
    print(tabulate({'ID':[i for i in range(1,len(products)+1)],'Name':[products[i]['name']for i in products],'Price':[products[i]['price']for i in products],'QTY':[products[i]['qty']for i in products],'Expiry':[products[i]['expiry']for i in products]},headers='keys', tablefmt='grid'))
def checkout(cart):      #to update the changes in dictionary
    for j in cart:
        products[j]['qty']=products[j]['qty']-cart[j]
def update(products,fname):    #to write the updated dictionary to json file
    r=json.dumps(products)
    f=open(f'{fname}.json','w')
    f.write(r)
    f.close()

cart={}     #to save selected items
price=[]    #to calculate total cost
qty_list=[] #to calculate total qty
sale_list=[]#to check for duplicate items and update qty
flag=True
display_p() #displaying table for customer
while flag:
    k_id=input('Enter ID:')
    if (k_id=='') or (int(k_id) not in range(1,len(products)+1)):   #to check for desired input
        print('Invalid ID')
        break
    k_id=int(k_id)
    qty=input('Enter quantity:')    
    if (qty==''):    #to check for desired input
        print('Invalid entry, quantity must be greater than 0')
        break
    p_id=str(keys[k_id])
    qty=int(qty)
    for i in sale_list:     #if duplicate item found update qty
        if p_id in i:
            qty=qty+i[1]
    if qty>products[p_id]['qty']:   #to check if the qty entered is greater than qty in inventory
        print('Sorry the selected item qty is less than what you have entered')
        break
    cart.update({p_id:qty})     #to save the entered item's id and qty entered
    sale_list.append([p_id,qty,str(datetime.now())[:16]])
    x=input('Checkout:Press C\t Continue:Press any key\n')
    x=x.lower()
    if x=='c':
        flag=False
if len(cart)==0:
    print('Check the values and try again, Thankyou')
    sys.exit()
for i in cart:
    pr=products[i]['price']*cart[i]
    qty_list.append(cart[i])
    price.append(pr)
total=sum(price)
print(tabulate({'Items':[i for i in range(1,len(cart)+1)],'Name':[products[i]['name']for i in cart],'QTY':[cart[i] for i in cart],'Price':[price[i] for i in range(0,len(cart))]},headers='keys',tablefmt='grid'))
print(tabulate({'Total Products':[sum(qty_list)],'Price':[total]},headers='keys',tablefmt='pretty'))
print(tabulate([{'Thankyou For Shopping,Visit Again'}]))
checkout(cart)      #to update the changes in dictionary
update(products,'plist')    #to write the updated dictionary to json file
try:
    sale_record=read('sales')
except:
    sale_record={} #sales record dictionary
sale_id=len(sale_record)
for i in sale_list:
    sale_id+=1
    sale_record.update({sale_id:{i[0]:{'name':products[i[0]]['name'],'qty':cart[i[0]],'amount':products[i[0]]['price']*cart[i[0]],'time':i[2]}}})

update(sale_record,'sales')