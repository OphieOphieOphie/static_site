from textnode import *
import htmlnode

def raw_text_to_markdown(text, line_tag="p"):
    length = len(text)
    
    opener_dict = {"*":"italic", "**":"bold", "***":"bold-italic", "`":"code", "[":"link", "![":"image"}
    closer_dict = {"italic":"*", "bold":"**", "bold-italic":("***","**","*"), "code":"`", "link":"]", "image":"]", "text":""}
    
    openers = "".join({y for i in opener_dict for y in i})
    current_closer = ""

    a = 0
    last = 0
    res = [["text"]]
    while a < length:

        ### this is how we know whether to close off the latest part of nested markdown

        if text[a] in current_closer:
            
            if a-1 >= 0 and text[a-1] == "\\": # if the previous character exists, and it's an escape character

                if a-2 >= 0 and last < a-1: # if it has anything before it
                    res[-1].append(text[last:a-1]) # we add that to the most recent block immediately
                last = a # we bring last forward to this point after the escape character
                
                if text[a] == "*": # *s are a special case 
                    peek_ahead = 1 # we need to see how many of them there are
                    while a + peek_ahead < length and text[a + peek_ahead] == "*" and peek_ahead < 4:
                        peek_ahead += 1
                    a += min(peek_ahead, 3) # the escape will ignore at most 3, since that's the highest valid combination of *s
                    continue

                if current_closer == text[a]:
                    a += 1
                    continue

            if text[a] != "*": # if it's not our bold/italics special case

                if text[a] == "]": # if it's a link/image format we ignore the first bracket
                    closer_dict[res[-1][0]] = ")" # we change the acceptable closer to ")"
                    current_closer = ")" # we update our current closer to it
                    a += 1 # move forward one to ignore this character

                    if a < length and text[a] != "(": # if the next character is not an opening parenthesis
                        raise Exception("Invalid Markdown, incorrect syntax, alt/link text declarations must be followed immediately by a link in parentheses")

                    continue

                if text[a] == ")": # we can't ignore this closer
                    closer_dict[res[-1][0]] = "]"

                if last != a: # if interior text (even a space) exists
                    res[-1].append(text[last:a]) # we add the previous sequence to the default (final) list in res (the last value has nothing to do with this, last refers to the next-to-be-added position in the text)
                    temp = res.pop()

                    if temp[0] == "link":
                        temp_data = "".join(temp[1:]).split("](")
                        temp = htmlnode.text_node_to_html_node(TextNode(text = temp_data[0], text_type = temp[0], url = temp_data[1])).to_html()
                    elif temp[0] == "image":
                        temp_data = "".join(temp[1:])
                        temp = htmlnode.text_node_to_html_node(TextNode(text = None, text_type = temp[0], url = temp_data)).to_html()
                    else:
                        temp_data = "".join(temp[1:])
                        temp = htmlnode.text_node_to_html_node(TextNode(text = temp_data, text_type = temp[0])).to_html()
                    
                    res[-1].append(temp)
                else: # if interior text does not exist
                    res.pop() # the last markdown opener is irrelevant
                
                current_closer = closer_dict[res[-1][0]] # we change our closer to the next one down

                a += 1 # once we're done with that, we move onto the next character
                last = a # and move our last index up to the current point

                continue # and immediately reset the loop
            
            peek_ahead = 1
            
            while a + peek_ahead < length and text[a + peek_ahead] == "*" and peek_ahead < 4:
                peek_ahead += 1

            if current_closer == ("***","**","*"): # if it's both bold and italic (we handle our special case separately)
                if peek_ahead >= 3:
                    if last != a or len(res[-1]) != 1:
                        res[-1].append(text[last:a])
                        res[-1][0], res[-2][0] = "bold", "italic"

                        temp = res.pop()

                        temp_data = "".join(temp[1:])
                        temp = htmlnode.text_node_to_html_node(TextNode(text = temp_data, text_type = temp[0])).to_html()
                        
                        res[-1].append(temp)

                        temp = res.pop()
                        
                        temp_data = "".join(temp[1:])
                        temp = htmlnode.text_node_to_html_node(TextNode(text = temp_data, text_type = temp[0])).to_html()

                        
                        res[-1].append(temp)
                    else:
                        res.pop()
                        res.pop()
                    
                    current_closer = closer_dict[res[-1][0]]

                    a += 3 # we only move forward 3, even if there's 4+ *s, since the next one could be another opener, even if bad practice
                    last = a
                    continue # and start the next loop early

                elif peek_ahead == 2:
                    if last != a or len(res[-1]) != 1:
                        res[-1].append(text[last:a])
                        res[-1][0], res[-2][0] = "bold", "italic"

                        temp = res.pop()
                        
                        temp_data = "".join(temp[1:])
                        temp = htmlnode.text_node_to_html_node(TextNode(text = temp_data, text_type = temp[0])).to_html()
                        
                        res[-1].append(temp)
                    else:
                        res.pop()
                        res[-1][0] = "italic" # otherwise, it would remain "bold_italic"
                    
                    current_closer = closer_dict[res[-1][0]]

                    a += 2 # we move forward 2, since we closed out a bolded instance
                    last = a
                    continue # and start the next loop early

                else: # peek_ahead == 1:
                    if last != a or len(res[-1]) != 1: # this tells us if the block would be empty or not
                        res[-1].append(text[last:a])
                        res[-1][0], res[-2][0] = "italic", "bold"

                        temp = res.pop()
                        
                        temp_data = "".join(temp[1:])
                        temp = htmlnode.text_node_to_html_node(TextNode(text = temp_data, text_type = temp[0])).to_html()
                        
                        res[-1].append(temp)
                    else:
                        res.pop()
                        res[-1][0] = "bold" # otherwise, it would remain "bold_italic"
                    
                    current_closer = closer_dict[res[-1][0]]

                    a += 1 # we move forward 1, since we closed out a italic instance
                    last = a
                    continue # and start the next loop early

            elif current_closer == "**":
                if peek_ahead == 1: # this is not a closer, this is an italic opener
                    pass # we let it continue and don't interact with the rest of the loop (we don't increment a and will get passed on to the opener if statement)

                else: # we don't care how many more than two it is, it's a closer, we're using it
                    if last != a or len(res[-1]) != 1: # this tells us if the block would be empty or not
                        res[-1].append(text[last:a])

                        temp = res.pop()
                        
                        temp_data = "".join(temp[1:])
                        temp = htmlnode.text_node_to_html_node(TextNode(text = temp_data, text_type = temp[0])).to_html()
                        
                        res[-1].append(temp)
                    else:
                        res.pop()
                    
                    current_closer = closer_dict[res[-1][0]]

                    a += 2 # we move forward 2, since we closed out a bolded instance
                    last = a
                    continue # and start the next loop early

            else: # current_closer == "*":
                if peek_ahead >= 2: # this is not a closer, this is a bold opener
                    pass # we let it continue and don't interact with the rest of the loop (we don't increment a and will get passed on to the opener if statement)
                else: # we don't care how many more than two it is, it's a closer, we're using it
                    if last != a or len(res[-1]) != 1: # this tells us if the block would be empty or not
                        res[-1].append(text[last:a])

                        temp = res.pop()
                        
                        temp_data = "".join(temp[1:])
                        temp = htmlnode.text_node_to_html_node(TextNode(text = temp_data, text_type = temp[0])).to_html()
                        
                        res[-1].append(temp)
                    else:
                        res.pop()
                    
                    current_closer = closer_dict[res[-1][0]]

                    a += 1 # we move forward 1, since we closed out an italic instance
                    last = a
                    continue # and start the next loop early
        
        ### this is how we know whether to open a new section of nested markdown
        
        if text[a] in openers:

            escaped = False
            
            if a-1 >= 0 and text[a-1] == "\\": # if the previous character exists, and it's an escape character
                if a-2 >= 0 and last < a-1: # if it has anything before it
                    res[-1].append(text[last:a-1]) # we add that to the most recent block immediately
                last = a # we bring last forward to this point after the escape character
                escaped = True

            if last != a:
                res[-1].append(text[last:a]) # we add the previous sequence to the default (last) list in res
                last = a

            start = a

            while a < length and text[a] in openers:

                a += 1

                if "".join(text[start: a]) in opener_dict: # if it's a valid opener
                    
                    if closer_dict["link"] == ")": # this prevents markdown from being initiated within the url sections
                        raise Exception("Invalid Markdown, no further markdown can be placed within link url")
                    elif closer_dict["image"] == ")": 
                        raise Exception("Invalid Markdown, no further markdown can be placed within image url")

                    if text[start] == "*": # nested bold/italics can present as "***"
                        
                        while a < length and a - start < 3 and text[a] == "*": # we need another loop to make sure we get all of them
                            a += 1
                    
                    if escaped:
                        break

                    markdown_symbol = "".join(text[start: a]) # we construct it
                    
                    current_identity = opener_dict[markdown_symbol] # we find out what it's called

                    if current_identity != "bold-italic":
                        res.append([current_identity]) # we append a new list to res. this is now the default. it starts with its identity.
                    else:
                        res.append([current_identity]) # "***" is a special case, since we don't know whether it's "**" + "*" or "*" + "**"
                        res.append([current_identity]) # we add it twice, and figure it out later

                    current_closer = closer_dict[current_identity] # and find and record its corresponding closer

                    last = a # we move our last index up to the current point

                    break # and we break out of the inner loop

                elif a-start > 3: # if it goes longer than 3 without being identified, it's invalid markdown
                    raise Exception("Invalid Markdown, symbol not recognized")
            
            continue # since we've already moved forward inside the loop to a potential non opening char, we don't want to move forward again

        a += 1
    
    if last != a:
        res[-1].append(text[last:a])

    if len(res) > 1:
        raise Exception("Invalid Markdown, opened symbols have not been closed")

    output = "".join(res[0][1:])

    return output

def line_splitter(document):
    def identity(x, ordered = False):
        
        first_space = x.find(" ")
        first_segment = x[:first_space]
        first_len = len(first_segment) + 1

        if x.startswith("1. ") or (ordered != False and first_segment[-1]=="." and first_segment[:-1].isdigit() ):
            return ("ol", first_len)
        elif first_segment == "*" or first_segment == "-":
            return ("ul", 2)
        elif first_segment in ("#","##","###","####","#####","######"):
            return (f"h{first_len - 1}", first_len)
        elif x.startswith(">"):
            return ("blockquote", 1)
        elif x.startswith("```") and x.endswith("```"):
            return ("code", 3)
        else: 
            return ("p", 0)
    
    split_document = list(filter(lambda x: not x=="", document.split("\n")[::-1]))
    line_starters = "1-*#>`"
    length = len(split_document)

    a = 0
    res = []
    while a < length:
        temp = []
        current = split_document.pop()
        current_id, current_offset = identity(current)
        temp.append(current[current_offset:])
        a += 1

        while a < length and split_document and current_id == identity(split_document[-1], current_id=="ol")[0]:
            if current_id == "ol":
                current_offset = identity(split_document[-1], True)[1]
            temp.append(split_document.pop()[current_offset:])
            a += 1
        res.append((current_id, temp))
    
    output = []
    for i in res:
        temp = []
        for c in i[1]:
            if i[0] == "code":
                temp.append(htmlnode.LeafNode(tag=None, value=raw_text_to_markdown(c[:-3])))
            elif i[0] in ("ul", "ol"):
                child = htmlnode.LeafNode(tag=None, value=raw_text_to_markdown(c))
                temp.append(htmlnode.ParentNode(tag="li", children=[child]))
            else:
                temp.append(htmlnode.LeafNode(tag=None, value=raw_text_to_markdown(c)))
        
        if i[0] == "code":
            block_strip = htmlnode.LeafNode(tag=None, value=htmlnode.ParentNode(tag="nil", children=temp).to_html().strip())

            inner_parent = htmlnode.ParentNode(tag="code", children=[block_strip])
            outer_parent = htmlnode.ParentNode(tag="pre", children=[inner_parent])
        else:
            block_strip = htmlnode.LeafNode(tag=None, value=htmlnode.ParentNode(tag="nil", children=temp).to_html().strip())

            outer_parent = htmlnode.ParentNode(tag=i[0], children=[block_strip])
        output.append(outer_parent)

    return htmlnode.ParentNode(tag="nil", children=output)

def markdown_to_html(document):
    split_document = list(filter(lambda x: not x=="", map(lambda x: x.strip() ,document.split("\n\n"))))
    res = []
    for i in split_document:
        if i.startswith("```") and i.endswith("```"):
            code_adjustment = i.split("\n")
            code_adjustment[0], code_adjustment[-1] = code_adjustment[0].replace("```", ""), code_adjustment[-1].replace("```", "")
            if code_adjustment[0] == "": code_adjustment.pop(0)
            if code_adjustment[-1] == "": code_adjustment.pop()
            code_leaf = htmlnode.LeafNode(tag=None, value=" ".join(code_adjustment))
            inner_parent = htmlnode.ParentNode(tag="code", children=[code_leaf])
            outer_parent = htmlnode.ParentNode(tag="pre", children=[inner_parent])
            res.append(outer_parent)
        else:
            res.append(line_splitter(i))
    return (htmlnode.ParentNode(tag="div", children=res).to_html())

def extract_title(document):
    split_document = list(filter(lambda x: not x=="", map(lambda x: x.strip() ,document.split("\n\n"))))
    for i in split_document:
        if i.startswith("# "):
            return i.replace("# ","").strip()
    raise Exception("No title found")