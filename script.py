# Script to rewrite the index.html to help update the website
import main, datetime, random

LAST_PLACE = 3
COLORS = [
    "#F7464A", "#46BFBD", "#FDB45C", "#949FB1", "#4D5360", "#A3E4D7",
    "#E74C3C", "#9B59B6", "#8E44AD", "#2980B9", "#3498DB", "#1ABC9C", "#16A085", "#27AE60",
    "#2ECC71", "#F1C40F", "#F39C12", "#BB8FCE", "#85C1E9", "#7DCEA0", "#F8C471"
] #22 COLORS, Add more if needed

COIN_COLOR = "#28B463"
DOLLAR_COLOR = "#2E86C1"

def leading_big(players:list) -> str:
    big = ""
    return max(players, key=lambda p: float(p.points)).name.title()

def most_coins(players:list) -> str:
    most_coins = max(players, key=lambda p: float(p.coins))
    return "{} (${:,.2f})".format(most_coins.name.title(), float(most_coins.coins))

def most_dollars(players:list) -> str:
    most_bills = max(players, key=lambda p: float(p.dollars))
    return "{} (${:,.2f})".format(most_bills.name.title(), float(most_bills.dollars))

def most_fundraised(players:list) -> str:
    most_fund = max(players, key=lambda p: p.dollars + p.coins)
    total = float(most_fund.dollars) + float(most_fund.coins)
    return "{} (${:,.2f})".format(most_fund.name.title(), total)

def calculate_total_fundraised(players: list) -> float:
    total = 0
    for p in players:
        total += (float(p.coins) + float(p.dollars))
    return total

def calculate_total_coins(players: list) -> float:
    total = 0
    for p in players:
        total += (float(p.coins))
    return total

def calculate_total_dollars(players: list) -> float:
    total = 0
    for p in players:
        total += (float(p.dollars))
    return total

def updateIndex_html(players: list, fileBase, fileIndex):
    total_fundraise_indicator = "<!--Input Total Amount Fundraised -->"
    fun_stats_indicator = "<!--Input Fun Stats -->"
    chart_data = "//Input Player Data Chart"
    chart_color = "//Input Player Color Chart"
    chart_label = "//Input Player Label Chart"
    chart_fund_data = "//Input Fundraise Data"
    chart_fund_color = "//Input Fundraise Color"
    chart_fund_label = "//Input Fundraise Label"
    date_indicator = "<!-- Input Updated Date -->"
    table_entry_indicator = "<!-- Table Entry Data -->"

    for line in fileBase.readlines():
        fileIndex.write(line)

        if total_fundraise_indicator in line:
            total = "${:,.2f}".format(calculate_total_fundraised(players))
            fileIndex.write("    			<h1 class=\"display-4\">{}</h1>\n".format(total))

        elif fun_stats_indicator in line:
            data = """
                	<h2 class="mb-5"> <i class="fas fa-angle-double-right"></i> Leading Big: {}</h1>
    				<h2 class="mb-5"> <i class="fas fa-angle-double-right"></i> Most Coins: {}</h1>
    				<h2 class="mb-5"> <i class="fas fa-angle-double-right"></i> Most Dollars: {}</h1>
    				<h2 class="mb-5"> <i class="fas fa-angle-double-right"></i> Most Fundraised: {}</h1>
    				\n""".format(leading_big(players),most_coins(players),most_dollars(players), most_fundraised(players))
            fileIndex.write(data)

        elif chart_data in line:
            for p in players:
                data = "                                        {},\n".format(float(p.coins) + float(p.dollars))
                fileIndex.write(data)

        elif chart_color in line:
            colorsList = COLORS
            random.shuffle(colorsList)
            for n in range(len(players)):
                data = "                                    \"{}\",\n".format(colorsList[n])
                fileIndex.write(data)

        elif chart_label in line:
            for p in players:
                percentage = (float(p.dollars) + float(p.coins)) / calculate_total_fundraised(players) * 100
                data = "                                    \"{} ({:.1f}%)\",\n".format(p.name.title(), percentage)
                fileIndex.write(data)

        elif chart_fund_data in line:
            dataCoins = "                                        {},\n".format(calculate_total_coins(players))
            dataBills = "                                        {},\n".format(calculate_total_dollars(players))
            fileIndex.write(dataCoins)
            fileIndex.write(dataBills)

        elif chart_fund_color in line:
            dataCoins = "                                        \"{}\",\n".format(COIN_COLOR)
            dataBills = "                                        \"{}\",\n".format(DOLLAR_COLOR)
            fileIndex.write(dataCoins)
            fileIndex.write(dataBills)

        elif chart_fund_label in line:
            coinPercentage = (calculate_total_coins(players)) / calculate_total_fundraised(players) * 100
            billPercentage = (calculate_total_dollars(players)) / calculate_total_fundraised(players) * 100
            dataCoins = "                                    \"Coins ({:.1f}%)\",\n".format(coinPercentage)
            dataBills = "                                    \"Bills ({:.1f}%)\",\n".format(billPercentage)
            fileIndex.write(dataCoins)
            fileIndex.write(dataBills)


        elif date_indicator in line:
            date = datetime.date.today().strftime("%B %d, %Y")
            data = "    			<p class=\"mb-0\">Updated Since {}</p>\n".format(date)
            fileIndex.write(data)

        elif table_entry_indicator in line:
            rank = 1
            for p in players:
                redTable = ""
                if rank + LAST_PLACE > len(players):
                    redTable = " class=\"table-danger\""
                data = """
                    <tr{last}>
                        <th scope="row">{rank}</th>
                        <td>{name}</td>
                        <td>{points}</td>
                        <td>{coins}</td>
                        <td>{dollars}</td>
                    </tr> \n""".format(rank=rank,name=p.name.title(),points="${:,.2f}".format(float(p.points)),
                                        coins="${:,.2f}".format(float(p.coins)),
                                        dollars="${:,.2f}".format(float(p.dollars)), last=redTable)
                fileIndex.write(data)
                rank += 1
    return


def mainScript():
    print("Running Script to Update Website...\n")

    date = datetime.date.today()
    date = date.strftime("%B %d, %Y")

    conn = main.create_connection(main.DB_FILE)
    main.create_table(conn)

    players = main.select_player_by_points(conn)

    fileBase = open("base.html", encoding="utf8")
    fileIndex = open("../index.html", "w", encoding="utf8")

    updateIndex_html(players, fileBase, fileIndex)

    main.print_table(conn)
    print("Website Updated as of {}".format(date))

if __name__ == '__main__':
    mainScript()