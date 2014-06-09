import bs4, requests, re, collections
import sys, thread, time
import string

def wiki_search(search_term):
    #print "Search Term: " + search_term
    
    # Get the wiki page and turn it into Beatiful Soup
    wiki_page = requests.get("http://en.wikipedia.org/wiki/" + search_term)
    wiki_soup = bs4.BeautifulSoup(wiki_page.content)
    summary_text = get_summary_text(wiki_soup)
    
    # Get the title of the wiki page
    title = wiki_soup.find('h1', class_='firstHeading').text
    
    # Print the title and summary text
    print "Title: " + title + '\n'
    print summary_text
    
    # Wait for the user to press Enter
    raw_input("-----Press Enter To Continue-----")
    print '\n'
    
    # Get the Table of Contents and print it
    toc = wiki_soup.find('div', class_='toc')
    
    toc_dict = {}
    toc_list = []
    create_toc(toc, toc_dict, toc_list)
    print_toc(toc_list)
    
def print_toc(toc_list):
    for (key, value) in toc_list:
        num_tabs = len(re.sub(r'[0-9]', '', key))
        print ('  ' * num_tabs) + key + ' - ' + value

def create_toc(toc_html, toc_dict, toc_list):
    temp_list = []
    
    # Get all lists from the Beautiful Soup
    for toc_item in toc_html.find_all('li'):
        # Print out the text for each link in each item
        for link in toc_item.find_all('a'):
            link_text = link.text.encode('utf-8')
            key = link_text.split(' ')[0]
            value = ' '.join(link_text.split(' ')[1:])
            toc_dict[key] = value
            temp_list.append((key, value))
    
    for item in temp_list:
        if item not in toc_list:
            toc_list.append(item)
            
    last_num = toc_list[-1:][0][0].split('.')[0]
    toc_dict[last_num] = "Search Again"
    # Passing (last_num + 1, "Search Again")
    toc_list.append((str( int (last_num) + 1 ), "Search Again"))
    #toc_list = temp_list

def get_summary_text(wiki_soup):
    # Get the location of where the summary is at
    summary_soup = wiki_soup.find('div', id='mw-content-text') 
    summary_text = []
    for element in summary_soup.find_all(True):
        # print element
        if element.name == 'p' and element.text != '':
            summary_text += element.text + '\n\n'
        if element.get('id') == 'toc':
            break
    return ''.join(summary_text)
            

def main(argv):
    wiki_search(argv[0])

if __name__ == '__main__':
    #Pass command line args to main
    main(sys.argv[1:])
