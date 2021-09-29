'''
This is for the purposes of balancing account credit with old account debt
Author: Robyn Proffer August 18
'''

## TODO

##

#used libraries and modules
from tabletools import DataBender
from tabletools import DataPrep
from credAccount import Account
class Creditor:
    
    def main():
        accounts = {}
        avatar = DataBender()
        nerd = DataPrep()
        data = avatar.Retrieve("Z:\BLSVRCOLAB\CREDITCARD.xlsx", 0)
        head = ['Account', 'OT', 'PRO', 'Credit balance', 'Open', 'Customer name', 'National account code', 'Date of most recent invoice', 'Date of last payment']
        heads = nerd.getHeading(head, data[0])
        print(data[0])
        print(heads)
        for i in data:
            #print(i)
            if i[heads['Account']] not in accounts:
                accounts[i[heads['Account']]] = Account(i[heads['Account']], heads)
            try:
                #if int(i[heads['Open']]) <= abs(int(i[heads['Credit balance']])) and int(i[heads['Open']])>0:
                accounts[i[heads['Account']]].addEntry(i)
            except Exception as e:
                print("rejected: " + str(e))
                print(i)
                continue
            
        for i in accounts:
            output = []
            if len(accounts[i].prose) == 0 or accounts[i].check == 0:
                continue
            print('**************************************************************************************************')
            print(accounts[i].viableEntries)
            for e in accounts[i].getPlan():
                p = e[1] #ensure Pro number is the proper length
                while len(p) < 10:
                    p = '0'+p
                e[1] = p
                output.append(e)
            print(output)
            avatar.putOut(output, "output/" + str(i) + ".XLSX", ['Account','Pro','Amount','Debt Considered','Applied Credit', 'Starting Credit', 'Initial Value'])
        print('done')    
            
    if __name__ == '__main__':    
        main()   