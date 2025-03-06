import pandas as pd

nationalities = ["A Vietnamese", "An American", "An Indian", "A German", "A Spaniard"]
monuments = []
monuments.extend(
    [
        "Meridian Gate of Huế",
        "Independence Palace",
        "One Pillar Pagoda",
        "Ho Chi Minh Mausoleum",
        "Thien Mu Pagoda",
    ]
)
monuments.extend(
    [
        "White House",
        "Statue of Liberty",
        "Mount Rushmore",
        "Golden Gate Bridge",
        "Lincoln Memorial",
    ]
)
monuments.extend(
    ["Taj Mahal", "Lotus Temple", "Gateway of India", "India Gate", "Charminar"]
)
monuments.extend(
    [
        "Cologne Cathedral",
        "Reichstag Building",
        "Neuschwanstein Castle",
        "Brandenburg Gate",
        "Holocaust Memorial",
    ]
)
monuments.extend(
    [
        "Sagrada Familia",
        "Alhambra",
        "Guggenheim Museum",
        "Roman Theater of Cartagena",
        "Royal Palace of Madrid",
    ]
)

age_gender = ["girl", "boy", "woman", "man", "old woman", "old man"]
df = pd.DataFrame(
    columns=["Image", "Keyword", "Age", "Gender", "Country", "Landmark", "Prompt"]
)
i = 1
with open("multilocations_prompts.txt", "w", encoding="utf-8") as file:
    for nation in nationalities:
        for person in age_gender:
            for monument in monuments:
                file.write(
                    f"{nation} {person} wearing traditional attire, standing in front of the {monument}.\n"
                )
                keyword = person.title()
                if person == "girl" or person == "boy":
                    age = "Young"
                elif person == "man" or person == "woman":
                    age = "Adult"
                else:
                    age = "Old"
                    keyword = keyword[4:]
                if person == "girl" or person == "woman" or person == "old woman":
                    gender = "Female"
                else:
                    gender = "Male"
                df = pd.concat(
                    [
                        df,
                        pd.DataFrame(
                            [
                                [
                                    f"{i}.png",
                                    keyword,
                                    age,
                                    gender,
                                    nation.split()[1],
                                    monument,
                                    f"{nation} {person} wearing traditional attire, standing in front of the {monument}.\n",
                                ]
                            ],
                            columns=df.columns,
                        ),
                    ],
                    ignore_index=True,
                )
                i += 1
df.to_excel('prompts.xlsx', index=False)
