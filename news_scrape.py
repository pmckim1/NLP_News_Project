#%%
# https://services.cnn.com/newsgraph/search/type:article
import json

import requests


class GuardianAccess():
    def __init__(self):
        self.api_key = "6f0112ea-0cb0-44bf-895b-445fcf3ec7aa"

    def search(self, session, term, section="world", production_office="US", from_date="2020-11-01", page=1):
        response = session.get(
            "https://content.guardianapis.com/search",
            params={
                "api-key": self.api_key,
                "q":term,
                "query-fields": "body",
                "from-date": from_date,
                "section": section,
                "production-office": production_office,
                "page": page,
            }
        )
        search_response = json.loads(response.text)
        # print(response.request.url)
        # print(response)
        # print(json.dumps(json_response, indent='\t'))
        return search_response

    def download_from_search(self, session, search_result):
        print("Attempting download")
        response = session.get(
            search_result["apiUrl"],
            params={
                "api-key": self.api_key,
                "show-blocks": "body",
            }
        )
        json_response = json.loads(response.text)

        # print(json.dumps(json_response, indent='\t'))
        
        bodyTextSummary = json_response["response"]["content"]["blocks"]["body"][0]["bodyTextSummary"]
        return bodyTextSummary

    def search_and_download(self, session, term):
        production_office="US"
        search_response = self.search(session, term, from_date="2020-11-01", production_office=production_office)
        print(json.dumps(search_response, indent='\t'))
        for page in range(search_response["response"]["pages"]):
            page=page + 1
            search_response = self.search(session, term, from_date="2020-11-01", production_office=production_office, page=page)
            #print(json.dumps(search_response, indent='\t'))

            for result in search_response["response"]["results"]:
                webTitle = result["webTitle"]
                if term.strip("\"") not in webTitle:
                    print("Skipping, because {} was not in it: {}".format(term, webTitle))
                    continue
                bodyTextSummary = self.download_from_search(session, result)


                webTitle = result["webTitle"]
                filename = "/Users/polly.mckim/Desktop/NewsArticles/" + webTitle + ".json"
                print("Saving: {}".format(filename))
                with open(filename, 'w', encoding="utf-8") as f:
                    f.write(
                        json.dumps(
                            {
                                "production_office": production_office,
                                "webPublicationDate": result["webPublicationDate"],
                                "text": bodyTextSummary,
                            }
                        )
                    )
              

if __name__=="__main__":
    ga = GuardianAccess()

    with requests.Session() as session:
        #ga.search_and_download(session, "\"Bill Gates\"")
         ga.search_and_download(session, "Trump")

 #ga.search_and_download(session, "\"Bill Gates\"")
# %%
