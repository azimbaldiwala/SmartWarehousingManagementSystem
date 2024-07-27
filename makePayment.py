

# this is dummy file 

def makePayment(cardname, cvv, name, exp, amount):
    print("Call payment api here")

    status = True # Value returned by api
    # api returns true if payment is done 

    if not status:
        return False 
    
    print("payment complete")

    return True