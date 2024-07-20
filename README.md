Web scraper for [Yoyochinese](https://yoyochinese.com/) premium subscribers.
Current Yoyochinese internal SRS Flashcards doesn't
use sentences inside the "Dialogue" tab for their cards.

This script retrieves information for each row inside the "Dialogue" tab: the sentence 
in Chinese and with pinyin, and the English translation. 
Additionally, it saves the accompanying MP3 files
and adds a "Tag" column. Then, it saves the data inside a CSV file 
for your own personal [Anki](https://apps.ankiweb.net/) deck.


## Anki
### Import MP3 files to Anki
_The MP3 file name and the Anki card audio field (saved inside CSV) must have the same name._
Anki audio field: `[sound:your-audio-file-name.mp3]`

Add MP3 files to Anki appdata folder on your local machine.

Example on MacOS:
> `Finder > Go > Go to Folder` 
> OR
> Inside _Finder_ `shift` + `cmd` + `G`


```
~/Library/Application Support/Anki2
```
More info here: https://docs.ankiweb.net/files.html

### Import CSV file to Anki
`Anki > File > Import`


# Notes
Make sure to be signed in for the webdriver to work
`driver = webdriver.Chrome()`
or provide additional option/args.


