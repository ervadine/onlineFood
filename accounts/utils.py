

def detectUser(user):
    if user.role==1:
        redirect="restaurant"
        return redirect
    elif user.role==2:
        redirect="customer"
        return redirect
    elif user.role==None and user.is_superuser:
        redirect="admin"
        return redirect
    
    
    
    
        
    
    
    