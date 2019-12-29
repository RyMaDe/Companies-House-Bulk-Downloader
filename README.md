# Companies-House-Bulk-Downloader
Allows you to view information on Companies House and download documents in bulk if required.

## Guide

1) You will require an API Key in order for this programme to work. This can
eaily be obtained for free from the Companies House website.

2) You must then save this API Key into the config.py document.

#### Features:

Return - Whilst using the programme, if you press enter without anything typed you will
be returned to the start of the programme. This will also happen if you type in an 
invalid command.

back - if you type "back" at any point in the programme it will take you back to
the previous page (unless you are searching for a term).

filter - When navigating the filing history, you can filter documents by typing
"filter" and then one of the following commands:

"accounts" - to filter all accounts
"officers" - to filter all officer documents
"confstat" - to filter all confirmation statements
"capital" - to filter all capital documents
"incorporation" - to filter incorporation documents
"charges" - to filter all charge related documents
"off" - to remove the filter

Navigating filing history - You can also type "next" and "prev" to navigate the
pages of the filing history. You can also type "page" followed by a space and a 
number.

Download all - You can download all of the documents being displayed on a page by typing
"all".
