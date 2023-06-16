import os
from datetime import datetime

## Function to generate the mesostic
def generate_mesostic(keyword, source_file):
    
    # Convert the keyword into an array, keeping spaces
    keyword_array = [ch for ch in keyword if ch.isalnum() or ch.isspace()]

    # Fetch the index positions for any spaces in the keyword array
    space_locations = [i for i, ch in enumerate(keyword_array) if ch.isspace()]

    # Convert the keyword into an array, omitting non-alphanumeric characters
    keyword_array = [ch for ch in keyword if ch.isalnum()]

    # Check if the keyword array is empty
    if not keyword_array:
        print("Error: keyword does not contain any alphanumeric characters.")
        return None

    # Convert the source file into an array of lines
    with open(source_file, 'r') as file:
        source_array = file.readlines()

    # Initialize an array to store the unformatted poem lines
    unformatted = []

    # Initialize indices for the keyword and source arrays
    keyword_index = 0
    source_index = 0

    while source_index < len(source_array):
        # If the keyword character is found in the source line
        if keyword_array[keyword_index].lower() in source_array[source_index].lower():
            # Add the line to the unformatted poem
            unformatted.append(source_array[source_index])

            # Move to the next keyword character
            keyword_index = (keyword_index + 1) % len(keyword_array)

        # Always move to the next source line
        source_index += 1
    
    # If the keyword was iterated without completing, remove excess lines
    while keyword_index > 0 and unformatted:
        unformatted.pop()  # Remove the last item from unformatted
        keyword_index -= 1  # Decrement keyword_index

    # Reset keyword_index to start with the first character in the keyword
    keyword_index = 0

   # Start the text formatting process
    lines = []
    for line in unformatted:
        keyword_char = keyword_array[keyword_index]
        if keyword_char.lower() in line.lower():
            # Find the keyword character and segment the line
            index = line.lower().index(keyword_char.lower())
            segmentation = [line[:index], line[index], line[index+1:]]

            # Capitalize the keyword character
            segmentation[1] = segmentation[1].upper()

            # For segmentation[0], we want to remove words from the beginning
            segmentation[0] = " ".join(segmentation[0].split()[-10:])

            # For segmentation[2], we want to remove words from the end
            segmentation[2] = " ".join(segmentation[2].split()[:10])
            
            # Append the segmentation to the lines list
            lines.append(segmentation)

            # Move to the next keyword character
            keyword_index = (keyword_index + 1) % len(keyword_array)

    # Start the display process
    poem = []
    for segmentation in lines:
        # Add the <b> tags around the keyword character
        segmentation[1] = '<b>' + segmentation[1] + '</b>'

        # Add the line to the poem
        poem.append(''.join(segmentation))

    # Convert the poem to a string and return it, along with front_spaces and back_spaces
    return poem, space_locations

## Main scripted user experience
def main():
    # Request a keyword
    keyword = input("Please enter a keyword: ")

    # Request a source file
    source_file = input("Please enter the path to a source file: ")

    # Ensure source file exists
    if not os.path.isfile(source_file):
        print("Error: file does not exist.")
        return
    
    # Generate mesostic and pass values
    mesostic, space_locations = generate_mesostic(keyword, source_file)

    # If the poem generation was successful
    if mesostic is not None:
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Create the output file name
        output_file_name = f"{keyword}_{timestamp}.html"
        # Create the output path
        dir_path = os.path.dirname(os.path.realpath(source_file))
        output_path = os.path.join(dir_path, output_file_name)

        with open('template.html', 'r') as file:
            html = file.read()

        # Initialize the mesostic poem html string
        mesostic_html = ''      
        
        keyword_index = 0  # Reset keyword_index
        
        # Add each line of the mesostic to the html string
        for i, line in enumerate(mesostic):
            
            if keyword_index == 0 and i != 0:  # check if it's not the very first line
                mesostic_html += '<p></p>'

            # If the line count matches a space location, add a blank line
            if keyword_index in space_locations:
                mesostic_html += '<p></p>'

            # Find the index of the bold character
            bold_index = line.index('<b>')

            # Create a div with two spans for the left and right parts of the line
            mesostic_html += f'<div class="line"><span class="left">{line[:bold_index]}</span><span class="right">{line[bold_index:]}</span></div>'
           
            # Move to the next keyword character
            keyword_index = (keyword_index + 1) % (len(keyword) - len(space_locations))

        # Insert the mesostic poem into the html string
        html = html.replace('<div class="mesostic"></div>', '<div class="mesostic">' + mesostic_html + '</div>', 1)

        with open(output_path, 'w') as file:
            file.write(html)
        print(f"The mesostic generation process is complete. The poem has been written to: {output_path}")

    else:
        print("Error: poem generation failed.")

if __name__ == "__main__":
    main()