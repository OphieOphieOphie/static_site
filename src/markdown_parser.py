from textnode import *
import htmlnode

def raw_text_to_markdown(text):
    length = len(text)

    openers = "*`[!"
    markdown_openers = {"*":"*", "**":"**", "`":"`", "[":")", "![":")"}
    opener_dict = {"*":"italic", "**":"bold", "`":"code", "[":"link", "![":"image"}

    a = 0
    last = 0
    res = []
    while a < length:
        if text[a] in openers and ord(text[max(0, a-1)]) != 92: # if we hit a markdown character, append the previous string (if any) as raw text
            if last != a:
                if res and res[-1][1] == "text": # the previous length of text wasn't long enough
                    res.pop() # remove it
                res.append((text[last:a],"text")) # add text to our results
            start = a # we store our starting point before we begin the inner loop
            while text[a] in openers:    
                a += 1
                if a >= length or text[a] not in openers: # if we get to the end of the string or if we reach a non-opener, we start our exit process
                    test_opener = "".join(text[start:a]) # we join our current string together from where we began up to now
                    if test_opener in markdown_openers: # if it's valid
                        closer = markdown_openers[test_opener] # we find out its corresponding closer
                        found = text[a+1:].find(closer) # and check if and where it exists
                        close_index = found + (a+1)
                        if found != -1 and ord(text[close_index-1]) != 92 : # if it exists
                            close_index = found + (a+1)
                            res.append((text[a:close_index], opener_dict[test_opener])) # we take it as a result
                            a = close_index + len(closer) # we increment our position
                            last = a # set that as the new starting point for default text strings
                            break # and end the loop
                        else:
                            break
                            #raise Exception("invalid markdown")
                    else:
                        # if it turns out to be a dud, we remove the last eronious entry (if added) from res and continue on
                        if last != a:
                            res.pop()
                        break
        a += 1
    if last + 1 < a:
        if res and res[-1][1] == "text":
            res.pop()
        res.append((text[last:length], "text"))
    for i, v in enumerate(res):
        if chr(92) in res[i][0]:
            bslsh = chr(92)
            repl = res[i][0]
            while f"{bslsh}*" in repl  or f"{bslsh}`" in repl or f"{bslsh}[" in repl  or f"{bslsh}![" in repl:
                repl = repl.replace(f"{bslsh}*","*").replace(f"{bslsh}`","`").replace(f"{bslsh}[","[").replace(f"{bslsh}![","![")
            res[i] = (repl, res[i][1])
        if res[i][1] == "image":
            res[i] = (f"![{res[i][0]}]", "image")

    for i, v in enumerate(res):
        if v[1] in ("text", "bold", "italic", "code"):
            res[i] = htmlnode.text_node_to_html_node(TextNode(v[0],v[1]))
        elif v[1] == "link":
            res[i] = htmlnode.text_node_to_html_node(TextNode(text = v[0].split("](")[0], text_type = v[1], url = v[0].split("](")[1]))
        else:
            res[i] = htmlnode.text_node_to_html_node(TextNode(text=None, text_type=v[1], url=v[0]))

    output = htmlnode.ParentNode(tag="p", children=res)

    return output.to_html()