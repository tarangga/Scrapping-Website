{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "name": "Function - www.jobinrwanda.com",
      "provenance": [],
      "mount_file_id": "1RtjCvHOfrvWurrzLjPxKyeRc4-vBzv4X",
      "authorship_tag": "ABX9TyPLefGOs1Y2JIdONzeWAEPc"
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "source": [
        "# Import Library"
      ],
      "metadata": {
        "id": "YYfZuL608Mb7"
      }
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "id": "3tVywFmi8Jui"
      },
      "outputs": [],
      "source": [
        "from requests import get, post\n",
        "from bs4 import BeautifulSoup as Soup\n",
        "import pandas as pd\n",
        "import re\n",
        "from json import loads, dumps"
      ]
    },
    {
      "cell_type": "markdown",
      "source": [
        "# Function"
      ],
      "metadata": {
        "id": "fFKpk7y48dyN"
      }
    },
    {
      "cell_type": "code",
      "source": [
        "def get_page(url):\n",
        "  try:\n",
        "    html = Soup(get(url).text)\n",
        "    job_url = html.find_all('small', {'class':'text-muted'})\n",
        "    record = {\n",
        "        'title': html.find('h5', {'class':'card-title'}).text,\n",
        "        'short_description': html.find('div', {'class': 'employer-description'}).text.strip() if html.find('div', {'class': 'employer-description'}) else '',\n",
        "        'rating': html.find('div', {'class': 'fivestar-summary fivestar-summary-average-count'}).text,\n",
        "        'job_url': job_url[1].text.strip() if len(job_url) > 1 else '',\n",
        "        'description': html.find('div', {'class':'field--name-field-job-full-description'}).text.strip()\n",
        "    }\n",
        "    return record\n",
        "  except Exception as e:\n",
        "    print(e, url)\n",
        "    return {}\n",
        "\n",
        "get_page('https://www.jobinrwanda.com/job/sales-officer-0')"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "uvOlwmLx8Xew",
        "outputId": "ce6b8591-c43d-4976-a26a-6605056fde8b"
      },
      "execution_count": 3,
      "outputs": [
        {
          "output_type": "execute_result",
          "data": {
            "text/plain": [
              "{'full_description': \"Job Description: Sales Officer\\nCompany Overview\\nGrand Investment &Trade Co. Ltd. was registered in Rwanda in 2019, has a commitment & vision to emerge in Rwanda and other Eastern African countries as the most trusted & committed spare parts supplier. We can supply spares ranging from commercial big trucks to small passenger cars with many companies in Rwanda and neighbouring countries.\\nJob Title:\\xa0Sales Officer\\nResponsibilities\\nFacilitate cold and warm calls to prospective leads; schedule and follow through on calls with leads and current customers within assigned territory\\nSource and work customer referrals\\nAnswer all lead and customer questions accurately; prioritize and/or escalate lead and customer questions as needed\\nPromote specific products as directed by upper management\\nInform leads and customers of current promotions and discounts\\nAnalyzing the market in terms of products and compare them to the competitors.\\nMaintain positive business and customer relationships in the effort to extend customer lifetime value\\nDevelop strategies for more effective sales, both individually and as part of a team\\nDesigning and implementing a strategic sales plan that expands the company’s customer base and ensures its strong presence.\\nHaving a good understanding of the business's products or services and be able to advise others about them\\nTrack all appointments, sales, complaints, status reports for manager review.\\nRequirements:\\nBachelor’s degree\\xa0\\nExcellent communication skills (verbal and written) in English & Kinyarwanda [French - Advantage]\\nQuick learner\\nAbility to multitask quickly and effectively\\nFull sales cycle, converting inbound prospects into clients\\nHardworking, honest, and patient\\nPioneer spirit (willing to grow with the company)\\nProduct sales, excellent Microsoft product knowledge and negotiation skills\\nNo criminal records\\nHow To Apply\\nInterested candidates should click the\\xa0Apply button\\xa0below to send their applications not later than\\xa024th April 2022\",\n",
              " 'job_url': '',\n",
              " 'rating': 'Average: 4.6 (12 votes)',\n",
              " 'short_description': 'Grand Investment &Trade Co. Ltd. was registered in Rwanda in 2019, has a commitment & vision to emerge in Rwanda and other Eastern African countries as the most trusted & committed spare parts supplier. We can supply spares ranging from commercial big trucks to small passenger cars with many companies in Rwanda and neighboring countries.\\nDriven by high-quality principles, high efficiency, and good service & ethical business practices, we are the company with inherent passion & commitment towards spares.',\n",
              " 'title': 'Grand Investment Trade Co Ltd'}"
            ]
          },
          "metadata": {},
          "execution_count": 3
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "url = 'https://www.jobinrwanda.com/'\n",
        "html = Soup(get(url).text)\n",
        "elements =html.find_all('div', {'class': 'card-body p-2'})"
      ],
      "metadata": {
        "id": "eGYO7pLM-0n-"
      },
      "execution_count": 4,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "def get_item(element):\n",
        "  employ = element.find('p', {'class':'card-text'})\n",
        "  return {\n",
        "    'item_url': 'https://www.jobinrwanda.com' + element.find('a')['href'],\n",
        "    'item_title': element.find('a').text.strip(),\n",
        "    'information': re.sub(r'[ \\r\\n\\t]+', ' ', employ.text).strip(),\n",
        "    'employe_url': 'https://www.jobinrwanda.com' + employ.a['href'],\n",
        "\n",
        "  }\n",
        "\n",
        "items = [get_item(el) for el in elements]"
      ],
      "metadata": {
        "id": "5UKHCNjJ_SdD"
      },
      "execution_count": 5,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "for item in items:\n",
        "  item.update(get_page(item['item_url']))"
      ],
      "metadata": {
        "id": "F7Dxoqe9B1rB"
      },
      "execution_count": 6,
      "outputs": []
    },
    {
      "cell_type": "code",
      "source": [
        "df = pd.DataFrame(items)\n",
        "df.to_csv('./temp_data-jobinrwanda.csv', index=False)"
      ],
      "metadata": {
        "id": "_4Uh7OG-DesD"
      },
      "execution_count": 7,
      "outputs": []
    }
  ]
}