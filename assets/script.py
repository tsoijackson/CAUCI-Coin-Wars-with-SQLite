# Script to rewrite the index.html to help update the website
import main, datetime

LAST_PLACE = 3

def leading_big(players:list) -> str:
    big = ""
    return max(players, key=lambda p: p.points).name.title()

def most_coins(players:list) -> str:
    most_coins = max(players, key=lambda p: p.coins)
    return "{} (${:,.2f})".format(most_coins.name.title(), float(most_coins.coins))

def most_dollars(players:list) -> str:
    most_bills = max(players, key=lambda p: p.dollars)
    return "{} (${:,.2f})".format(most_bills.name.title(), float(most_bills.dollars))

def most_fundraised(players:list) -> str:
    most_fund = max(players, key=lambda p: p.dollars + p.coins)
    total = float(most_fund.dollars) + float(most_fund.coins)
    return "{} (${:,.2f})".format(most_fund.name.title(), total)

def calculate_total_fundraised(players: list) -> str:
    total = 0
    for p in players:
        total += (float(p.coins) + float(p.dollars))
    return "${:,.2f}".format(total)

def updateIndex_html(players: list, fileBase, fileIndex):
    total_fundraise_indicator = "<!--Input Total Amount Fundraised -->"
    fun_stats_indicator = "<!--Input Fun Stats -->"
    pie_chart_indicator = "//Input Pie Chart Data"
    date_indicator = "<!-- Input Updated Date -->"
    table_entry_indicator = "<!-- Table Entry Data -->"

    for line in fileBase.readlines():
        fileIndex.write(line)

        if total_fundraise_indicator in line:
            total = calculate_total_fundraised(players)
            fileIndex.write("    			<h1 class=\"display-4\">{}</h1>\n".format(total))

        elif fun_stats_indicator in line:
            data = """
                	<h1 class="display-5 mb-3"> <i class="fas fa-angle-double-right"></i> Leading Big: {}</h1>
    				<h1 class="display-5 mb-3"> <i class="fas fa-angle-double-right"></i> Most Coins: {}</h1>
    				<h1 class="display-5 mb-3"> <i class="fas fa-angle-double-right"></i> Most Dollars: {}</h1>
    				<h1 class="display-5 mb-3"> <i class="fas fa-angle-double-right"></i> Most Fundraised: {}</h1>
    				\n""".format(leading_big(players),most_coins(players),most_dollars(players), most_fundraised(players))
            fileIndex.write(data)

        elif pie_chart_indicator in line:
            for p in players:
                data = "					  ['{name}', {total}],\n".format(name=p.name.title(),
                                                                         total = float(p.coins) + float(p.dollars))
                fileIndex.write(data)

        elif date_indicator in line:
            date = datetime.date.today().strftime("%B %d, %Y")
            data = "    			<p class=\"mb-0\">Updated Since January {}</p>\n".format(date)
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