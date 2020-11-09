class TreeNode: 
    def __init__(self,key):
        self.key=key
        self.left=None
        self.right=None
        self.parent=None

class SplayTree:
    def __init__(self):
        self.root=None
                    
    def insert(self, key):
        z = TreeNode(key)
        y = None
        x = self.root
        while x!= None:
            y = x
            if key < x.key:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y == None:
            self.root = z
        elif key < y.key:
            y.left = z
            self.root = self.splay(z)
        else:
            y.right = z
            self.root = self.splay(z)
            
    def left_rotate(self, node): #node: the node originally on the top
        y = node.right
        node.right = y.left
        if y.left != None:
            y.left.parent = node
        y.parent = node.parent
        
        if node.parent == None:
            self.root = y
        elif node == node.parent.left:
            node.parent.left = y
        else:
            node.parent.right = y
        y.left = node
        node.parent = y
        
    def right_rotate(self, node):
        y = node.left
        node.left = y.right
        if y.right != None:
            y.right.parent = node
        y.parent = node.parent
        
        if node.parent == None:
            self.root = y
        elif node == node.parent.right:
            node.parent.right = y
        else:
            node.parent.left = y
        y.right = node
        node.parent = y
    
    def splay(self, node):  #node: the node we want to move to root
        if node == self.root:
            return node
        
        while node.parent != None: #node is not at the root
            if node.parent == self.root:  #node is one of the chils of the root
                if node.key < self.root.key:
                    self.right_rotate(self.root)
                else:
                    self.left_rotate(self.root)
            else:
                if node.key < node.parent.key and node.parent.key < node.parent.parent.key: #left-left
                    self.right_rotate(node.parent.parent)
                    self.right_rotate(node.parent)
                elif node.key > node.parent.key and node.parent.key < node.parent.parent.key: #left-right
                    self.left_rotate(node.parent)
                    self.right_rotate(node.parent)
                elif node.key < node.parent.key and node.parent.key > node.parent.parent.key: #right-left
                    self.right_rotate(node.parent)
                    self.left_rotate(node.parent)
                else:    #right-right
                    self.left_rotate(node.parent.parent)
                    self.left_rotate(node.parent)              
        self.root = node  
        return node
                
    def Preorder(self):
        def recursivePreorder(node):
            if not node:
                return
            yield node.key
            yield from recursivePreorder(node.left)
            yield from recursivePreorder(node.right)

        return recursivePreorder(self.root)
    
    def Inorder(self):
        def recursiveInorder(node):
            if not node:
                return
            yield from recursiveInorder(node.left)
            yield node.key
            yield from recursiveInorder(node.right)

        return recursiveInorder(self.root)

def insert_compare(compare, num):   
    count = 0   
    for j in range(len(compare)-1, -1, -1):
        if compare[j] > num:
            break
        else:
            count = count + 1
    for j in range(count):
        compare.pop()
    compare.append(num)
    return compare

def check_compare(compare, num):   
    count = 0   
    for j in range(len(compare)-1, -1, -1):
        if compare[j] > num:
            break
        else:
            count = count + 1
    for j in range(count):
        compare.pop()
        
def num_bigger(compare, num):   
    count = 0   
    for j in range(len(compare)-1, -1, -1):
        if compare[j] > num:
            break
        else:
            count = count + 1
    return count

def check_stack(result):
    stack = []
    j = 0
    while j < len(result):
        stack.append(result[j])
        if result[j] == ')':
            stack.pop()
            stack.pop()
            stack.pop()
            stack.pop()
        
        if len(stack) > 3:
            while (stack[-1]=='-' or type(stack[-1])==int) and (stack[-2]=='-' or type(stack[-2])==int) and (stack[-3]=='-' or type(stack[-3])==int):               
                result.insert(j, ')')
                j = j + 1
                #print(stack)
                stack.pop()
                stack.pop()
                stack.pop()
                stack.pop()
                stack.append(result[j])
                #if len(stack) < 4:
                #    break
                
        if j == len(result) - 1:
            while len(stack) > 1: 
                if (stack[-1]=='-' or type(stack[-1])==int) and (stack[-2]=='-' or type(stack[-2])==int):
                    result.append(')')
                    j = j + 1
                    #print(stack)
                    stack.pop()
                    stack.pop()
                    stack.pop()
                else:
                    result.append('-')
                    result.append(')')
                    j = j + 2
                    stack.pop()
                    stack.pop()
                
        j = j + 1
    return result          
  

def parenthesis(pre):
    result = []
    compare = []
    result.append(pre[0])
    
    i = 1
    while i < len(pre): 
        if pre[i] < pre[i-1]:
            result.append('(')
            #compare.append(result[-2])
            insert_compare(compare, result[-2])
            result.append(pre[i])
            
        else:
            if num_bigger(compare, pre[i]) == 0:
                result.append('(')
                insert_compare(compare, result[-2])
                result.append('-')
                result.append(pre[i])
                check_compare(compare, result[-1])
            elif num_bigger(compare, pre[i]) == 1:
                result.append(pre[i])
                check_compare(compare, result[-1])

            else:    
                for j in range(num_bigger(compare, pre[i])-1):
                    result.append('-')
                    result.append(')')
                result.append(pre[i])
                check_compare(compare, result[-1])   
        i = i + 1
    result = check_stack(result)           
    return result

def left_bdry(points):
    x = -1  
    left_bdry = []
    left_bdry.append(points[0][0])
    for j in range(len(points)):
        if j != 0 and points[j][2] != points[j-1][2]:
            left_bdry.append(points[j][0])
    return left_bdry

def print_tree_left_bdry(points):
    x = -1  #a number that will never intersect with the x-axis
    left_bdry = []
    left_bdry.append(points[0][0])
    for j in range(len(points)):
        if j != 0 and points[j][2] != points[j-1][2]:
            print('\n', end='')
            x = -1
            left_bdry.append(points[j][0])
            
        #if x == -1:
        #    for k in range(points[j][1]):
        #        print('   ', end='')
        if points[j][1]-x-1 != 0:   #this will hold even if x = -1
            for k in range(points[j][1]-x-1):
                print('   ', end='')
                
        x = points[j][1]
        
        if points[j][0]>=1 and points[j][0]<=9:
            print(points[j][0], '  ', sep='', end='')
        elif points[j][0]>=10 and points[j][0]<=99:
            print(points[j][0], ' ', sep='', end='')
        else:
            print(points[j][0], end='')
    return left_bdry

# read file
file = open('/Users/Desktop/data stucture/Prog1_note/input.txt', 'r')  #change to your own directory
input_data = []
for line in file.readlines():
    line = line[:-1].split()
    line_int = [int(x) for x in line]
    input_data.append(line_int)
file.close()

#run given data
STree_ans1 = []
STree_ans3 = []
file2 = open('/Users/Desktop/data stucture/answer/STree.txt', 'w')   #change to your own directory
for w in range(len(input_data)):
    Tree=SplayTree()   
    for i in range(len(input_data[w])):
        Tree.insert(input_data[w][i])
    preorder = []
    inorder = []
    for i in Tree.Preorder():
        preorder.append(i)
    for i in Tree.Inorder():
        inorder.append(i)
    
    ans_1 = parenthesis(preorder)
    ans_1_no_space = []
    for i in range(len(ans_1)):
        ans_1_no_space.append(ans_1[i])  
        
    #if we don't need the space between two parentheses
    k = 1
    while k < len(ans_1):
        if (ans_1[k]=='-' or type(ans_1[k])==int) and (ans_1[k-1]=='-' or type(ans_1[k-1])==int):
            ans_1.insert(k, ' ')
            k = k + 1
        k = k + 1
    STree_ans1.append(ans_1)  #ans 1

    x_axis = []
    for j in range(len(preorder)):   
        index = inorder.index(preorder[j])
        x_axis.append(index)

    stack_2 = []
    y_axis = []
    for j in range(len(ans_1_no_space)):
        if ans_1_no_space[j] == ')':
            stack_2.pop()
            stack_2.pop()
            stack_2.pop()
            #print(stack_2)
        else:
            stack_2.append(ans_1_no_space[j])
            #print(stack_2)
    
        if type(ans_1_no_space[j]) == int: 
            count = 0   #root is in layer 0
            for k in range(len(stack_2)):
                if stack_2[k] == '(':
                    count = count + 1
            y_axis.append(count)  
            
    points = []   #the elements in points are (key, x_axis, y_axis)
    for j in range(len(preorder)):
        points.append([preorder[j], x_axis[j], y_axis[j]])
    points = sorted(points, key = lambda A: (A[2], A[1]))  #first sort y, then sort x
    ans_3 = left_bdry(points)
    STree_ans3.append(ans_3)   #ans 3
    
    x = -1
    for j in range(len(points)):
        if j != 0 and points[j][2] != points[j-1][2]:
            file2.write('\n')
            x = -1   
        if points[j][1]-x-1 != 0:  
            for k in range(points[j][1]-x-1):
                file2.write('   ')
                
        x = points[j][1]
        
        if points[j][0]>=1 and points[j][0]<=9:
            file2.write(str(points[j][0]) + '  ')
        elif points[j][0]>=10 and points[j][0]<=99:
            file2.write(str(points[j][0]) + ' ')
        else:
            file2.write(str(points[j][0]))
    file2.write('\n')
file2.close()

#write ans 1
file1 = open('/Users/Desktop/data stucture/answer/STree_PRep.txt', 'w')  #change to your own directory
for i in range(len(STree_ans1)):
    for j in range(len(STree_ans1[i])):
        if j == 0:
            file1.write(str(STree_ans1[i][j]))
        else:
            file1.write('' + str(STree_ans1[i][j]))
    file1.write('\n')
file1.close()

#write ans 3
file3 = open('/Users/Desktop/data stucture/answer/STree_boundary.txt', 'w')   #change to your own directory
for i in range(len(STree_ans3)):
    for j in range(len(STree_ans3[i])):
        if j == 0:
            file3.write(str(STree_ans3[i][j]))
        else:
            file3.write(' ' + str(STree_ans3[i][j]))
    file3.write('\n')
file3.close()