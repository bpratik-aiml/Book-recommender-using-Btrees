
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.views.decorators.csrf import csrf_protect


# Create your views here.
def register(request):
    return render(request, 'registration.html')
def signin(request):
    # firstname = request.POST['First_Name']
    # lastname = request.POST['Last_Name']
    # contact_1 = request.POST['Contact']
    # email = request.POST['E-mail']
    # city = request.POST['City']
    # username = request.POST['Username']
    # password = request.POST['Password']
    # #user = User.objects.create_user(username = username, email = email, password= password, first_name = firstname, last_name = lastname )
    # user = User(username = username, email = email, password= password, first_name = firstname, last_name = lastname )
    # user.save()
    # print("user created")
    
    return render(request, 'login.html')
    pass

def login_db(request):
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")
  
# Database Name
    db = client["ADS_books"]
  
# Collection Name
    col = db["auth_user"]
   # x = col.find()
  

    if request.method == "POST":
        username1 = (request.POST['username'])
        password1 = (request.POST['password'])

        myquery ={"username" : username1, "password" :password1}
        user = col.find_one({'username' : username1, 'password' : password1})
        #print(username, password)
        # user = authenticate(request, username = username1, password = password1)
        print (user)
        # for x in user:
        #     print("Hello" ,x)
        if user is not None:
            #form = auth.login(request, user)
            return render(request, 'index.html',{'name':username1, "flag":True})
        else:
            HttpResponse("Log In failed.")
            return render(request, 'login.html',{'error':"Hello user you entered wrong credentials. Please try again!"})



    return HttpResponse("Inserted")
    #return render(request, '')

#@csrf_protect
def book_data(request):
    #csrfContext = RequestContext(request)
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['ADS_books']
    col = db['books']
     
    title = (request.POST['title'])
    genre = (request.POST['book-genre'])
    url = (request.POST['book-url'])
    description = (request.POST['book-description'])
    author = (request.POST['author_name'])
    rating = (request.POST['rating'])

    doc = {
    "title":title,
    "genre":genre,
    "url":url,
    "description":description,
    "author": author,
    "rating": rating,
    }
    x = (col.insert_one(doc))
    print(x.inserted_id)
    return render(request, 'index.html')

def search(request):
    import pymongo
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    db = client['ADS_books']
    col = db['books']

    title = request.POST['title']
    genre = request.POST['book-genre']
    author = request.POST['author']


    list_of_books = []
    # for i in col.find({},{"name":1,'_id':0,"author":1}):
    #     print(i)
    #     list_of_books.append(i['name'])
    #     list_of_books.append(i['author'])
    #     print()
# B+ tee in python
# B+ tee in python


    import math

# Node creation
    class Node:
        def __init__(self, order):
            self.order = order
            self.values = []
            self.keys = []
            self.nextKey = None
            self.parent = None
            self.check_leaf = False

    # Insert at the leaf
        def insert_at_leaf(self, leaf, value, key):
            if (self.values):
                temp1 = self.values
                for i in range(len(temp1)):
                    if (value == temp1[i]):
                        self.keys[i].append(key)
                        break
                    elif (value < temp1[i]):
                        self.values = self.values[:i] + [value] + self.values[i:]
                        self.keys = self.keys[:i] + [[key]] + self.keys[i:]
                        break
                    elif (i + 1 == len(temp1)):
                        self.values.append(value)
                        self.keys.append([key])
                        break
            else:
                self.values = [value]
                self.keys = [[key]]


# B plus tree
    class BplusTree:
        def __init__(self, order):
            self.root = Node(order)
            self.root.check_leaf = True

    # Insert operation
        def insert(self, value, key):
            value = str(value)
            old_node = self.search(value)
            old_node.insert_at_leaf(old_node, value, key)

            if (len(old_node.values) == old_node.order):
                node1 = Node(old_node.order)
                node1.check_leaf = True
                node1.parent = old_node.parent
                mid = int(math.ceil(old_node.order / 2)) - 1
                node1.values = old_node.values[mid + 1:]
                node1.keys = old_node.keys[mid + 1:]
                node1.nextKey = old_node.nextKey
                old_node.values = old_node.values[:mid + 1]
                old_node.keys = old_node.keys[:mid + 1]
                old_node.nextKey = node1
                self.insert_in_parent(old_node, node1.values[0], node1)

    # Search operation for different operations
        def search(self, value):
            current_node = self.root
            while(current_node.check_leaf == False):
                temp2 = current_node.values
                for i in range(len(temp2)):
                    if (value == temp2[i]):
                        current_node = current_node.keys[i + 1]
                        break
                    elif (value < temp2[i]):
                        current_node = current_node.keys[i]
                        break
                    elif (i + 1 == len(current_node.values)):
                        current_node = current_node.keys[i + 1]
                        break
            return current_node

    # Find the node
        def find(self, value, key):
            l = self.search(value)
            for i, item in enumerate(l.values):
                if item == value:
                    if key in l.keys[i]:
                        return True
                    else:
                        return False
            return False

    # Inserting at the parent
        def insert_in_parent(self, n, value, ndash):
            if (self.root == n):
                rootNode = Node(n.order)
                rootNode.values = [value]
                rootNode.keys = [n, ndash]
                self.root = rootNode
                n.parent = rootNode
                ndash.parent = rootNode
                return

            parentNode = n.parent
            temp3 = parentNode.keys
            for i in range(len(temp3)):
                if (temp3[i] == n):
                    parentNode.values = parentNode.values[:i] + \
                        [value] + parentNode.values[i:]
                    parentNode.keys = parentNode.keys[:i +
                                                      1] + [ndash] + parentNode.keys[i + 1:]
                    if (len(parentNode.keys) > parentNode.order):
                        parentdash = Node(parentNode.order)
                        parentdash.parent = parentNode.parent
                        mid = int(math.ceil(parentNode.order / 2)) - 1
                        parentdash.values = parentNode.values[mid + 1:]
                        parentdash.keys = parentNode.keys[mid + 1:]
                        value_ = parentNode.values[mid]
                        if (mid == 0):
                            parentNode.values = parentNode.values[:mid + 1]
                        else:
                            parentNode.values = parentNode.values[:mid]
                        parentNode.keys = parentNode.keys[:mid + 1]
                        for j in parentNode.keys:
                            j.parent = parentNode
                        for j in parentdash.keys:
                            j.parent = parentdash
                        self.insert_in_parent(parentNode, value_, parentdash)

    # Delete a node
        def delete(self, value, key):
            node_ = self.search(value)

            temp = 0
            for i, item in enumerate(node_.values):
                if item == value:
                    temp = 1

                    if key in node_.keys[i]:
                        if len(node_.keys[i]) > 1:
                            node_.keys[i].pop(node_.keys[i].index(key))
                        elif node_ == self.root:
                            node_.values.pop(i)
                            node_.keys.pop(i)
                        else:
                            node_.keys[i].pop(node_.keys[i].index(key))
                            del node_.keys[i]
                            node_.values.pop(node_.values.index(value))
                            self.deleteEntry(node_, value, key)
                    else:
                        print("Value not in Key")
                        return
            if temp == 0:
                print("Value not in Tree")
                return

    # Delete an entry
        def deleteEntry(self, node_, value, key):

            if not node_.check_leaf:
                for i, item in enumerate(node_.keys):
                    if item == key:
                        node_.keys.pop(i)
                        break
                for i, item in enumerate(node_.values):
                    if item == value:
                        node_.values.pop(i)
                        break

            if self.root == node_ and len(node_.keys) == 1:
                self.root = node_.keys[0]
                node_.keys[0].parent = None
                del node_
                return
            elif (len(node_.keys) < int(math.ceil(node_.order / 2)) and node_.check_leaf == False) or (len(node_.values) < int(math.ceil((node_.order - 1) / 2)) and node_.check_leaf == True):

                is_predecessor = 0
                parentNode = node_.parent
                PrevNode = -1
                NextNode = -1
                PrevK = -1
                PostK = -1
                for i, item in enumerate(parentNode.keys):

                    if item == node_:
                        if i > 0:
                            PrevNode = parentNode.keys[i - 1]
                            PrevK = parentNode.values[i - 1]

                        if i < len(parentNode.keys) - 1:
                            NextNode = parentNode.keys[i + 1]
                            PostK = parentNode.values[i]

                if PrevNode == -1:
                    ndash = NextNode
                    value_ = PostK
                elif NextNode == -1:
                    is_predecessor = 1
                    ndash = PrevNode
                    value_ = PrevK
                else:
                    if len(node_.values) + len(NextNode.values) < node_.order:
                        ndash = NextNode
                        value_ = PostK
                    else:
                        is_predecessor = 1
                        ndash = PrevNode
                        value_ = PrevK

                if len(node_.values) + len(ndash.values) < node_.order:
                    if is_predecessor == 0:
                        node_, ndash = ndash, node_
                    ndash.keys += node_.keys
                    if not node_.check_leaf:
                        ndash.values.append(value_)
                    else:
                        ndash.nextKey = node_.nextKey
                    ndash.values += node_.values

                    if not ndash.check_leaf:
                        for j in ndash.keys:
                            j.parent = ndash

                    self.deleteEntry(node_.parent, value_, node_)
                    del node_
                else:
                    if is_predecessor == 1:
                        if not node_.check_leaf:
                            ndashpm = ndash.keys.pop(-1)
                            ndashkm_1 = ndash.values.pop(-1)
                            node_.keys = [ndashpm] + node_.keys
                            node_.values = [value_] + node_.values
                            parentNode = node_.parent
                            for i, item in enumerate(parentNode.values):
                                if item == value_:
                                    p.values[i] = ndashkm_1
                                    break
                        else:
                            ndashpm = ndash.keys.pop(-1)
                            ndashkm = ndash.values.pop(-1)
                            node_.keys = [ndashpm] + node_.keys
                            node_.values = [ndashkm] + node_.values
                            parentNode = node_.parent
                            for i, item in enumerate(p.values):
                                if item == value_:
                                    parentNode.values[i] = ndashkm
                                    break
                    else:
                        if not node_.check_leaf:
                            ndashp0 = ndash.keys.pop(0)
                            ndashk0 = ndash.values.pop(0)
                            node_.keys = node_.keys + [ndashp0]
                            node_.values = node_.values + [value_]
                            parentNode = node_.parent
                            for i, item in enumerate(parentNode.values):
                                if item == value_:
                                    parentNode.values[i] = ndashk0
                                    break
                        else:
                            ndashp0 = ndash.keys.pop(0)
                            ndashk0 = ndash.values.pop(0)
                            node_.keys = node_.keys + [ndashp0]
                            node_.values = node_.values + [ndashk0]
                            parentNode = node_.parent
                            for i, item in enumerate(parentNode.values):
                                if item == value_:
                                    parentNode.values[i] = ndash.values[0]
                                    break

                    if not ndash.check_leaf:
                        for j in ndash.keys:
                            j.parent = ndash
                    if not node_.check_leaf:
                        for j in node_.keys:
                            j.parent = node_
                    if not parentNode.check_leaf:
                        for j in parentNode.keys:
                            j.parent = parentNode


# Print the tree
    def printTree(tree):
        lst = [tree.root]
        level = [0]
        leaf = None
        flag = 0
        lev_leaf = 0

        node1 = Node(str(level[0]) + str(tree.root.values))

        while (len(lst) != 0):
            x = lst.pop(0)
            lev = level.pop(0)
            if (x.check_leaf == False):
                for i, item in enumerate(x.keys):
                    print(item.values)
            else:
                for i, item in enumerate(x.keys):
                    print(item.values)
                if (flag == 0):
                    lev_leaf = lev
                    leaf = x
                    flag = 1


    record_len = 3
#x = list_of_books[1]
#y = "A"
    bplustree = BplusTree(record_len)
#bplustree.insert(x, y)
    bplustree.insert('5', '33')
    bplustree.insert('15', '21')
    bplustree.insert('25', '31')
    bplustree.insert('35', '41')
    bplustree.insert('45', '10')

    for i in col.find({},{"title":1,'_id':0,"author":1}):
        print(i)
        bplustree.insert(i['title'], i['author'])
        #print(i['title'], i['author'])

    
    printTree(bplustree)
    if(bplustree.find(title, author)):
        print("Found")
        data = col.find_one({'title':title,'author':author})
        title = data['title']
        genre=data['genre']
        description = data['description']
        author = data['author']
        rating = data['rating']
        url = data['url']
        return render(request, 'index.html',{'title':title, 'genre':genre, 'author':author, 'rating':rating, 'url':url})

    else:
        print("Not Found")
    
    
    # if(bplustree.find(x, "A")):
    #     print("Found")
    # else:
    #     print("Not found")



   # return render(request, 'index.html')