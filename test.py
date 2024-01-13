print("hello world")

topicInput = "" # string of the topic
citationFormat = "" # string of the format of citation (MLA, APA, Chicago)
numberSources = 0 # how many sources are to be returned (maximum of 6)

print("testing 2FA")

response = "Title: here Citation: citation Title: here2 Citation: citation2"

miniresponse = response
for i in range(numSources):
    j = 0
    while j != i:
        miniresponse = response[response.find("Title:")+1:]

    miniresponse = miniresponse[miniresponse.find("Title:"):]

    title = miniresponse[miniresponse.find("Title:") : miniresponse.find("Link:")]
    url = miniresponse[miniresponse.find("Link:")+5 : miniresponse.find("Summary:")]
    summary = miniresponse[miniresponse.find("Summary:") : miniresponse.find("Citation:")]
    citation = miniresponse[miniresponse.find("Citation:") : miniresponse[1:].find("Title:")]

    title = title.replace("*", "")
    url = url.replace("*", "")
    summary = summary.replace("*", "")
    citation = citation.replace("*", "")
