# espn-ff-gotw

Determine my fantasy football league's game of the week.

## Using the ESPN API for Fantasy Football

ESPN provides a public API for accessing fantasy football information about your league, team, players, etc.

## Python > `espn-api`

There are several repos that have projects to leverage the ESPN API for fantasy football. I went with python-based `espn-api` which has a [really good wiki](https://github.com/cwendt94/espn-api/wiki/Football-Intro) to get started.

> [https://github.com/cwendt94/espn-api](https://github.com/cwendt94/espn-api)

### Install

On a Mac, use `homebrew` to install `python3` and `pip3`.

Then use `pip3` to install the `espn-api` package:

```bash
pip3 install espn-api
```

### Usage

Refer to the [Football Intro Wiki](https://github.com/cwendt94/espn-api/wiki/Football-Intro) for examples, syntax, and more.

For private leagues, you'll need to get two cookies' values from your browser to authenticate into your league: `SWID` and `espn_s2`.

### jq

The ESPN API returns data in compact JSON format. The `jq` utility is useful for detailed and specific parsing of elements. In this case, I just want it prettified on multiple lines to cheat with a simple `grep`. But for more advanced JSON spelunking, it'll come in handy.

> [https://jqlang.github.io/jq/manual/](https://jqlang.github.io/jq/manual/)

## gotw.py

This python program will determine the league's game of the week. It counts the number of players on every fantasy team's roster and adds them up for the games this week.

Specify the week number on the command-line, or it defaults to week 1.

```bash
python3 gotw.py 1
```

Returns unordered results similar to:

```log
15 FF league players in wk 1 game: DET @ KC
12 FF league players in wk 1 game: CAR @ ATL
13 FF league players in wk 1 game: CIN @ CLE
14 FF league players in wk 1 game: JAX @ IND
14 FF league players in wk 1 game: TB @ MIN
15 FF league players in wk 1 game: TEN @ NO
15 FF league players in wk 1 game: SF @ PIT
16 FF league players in wk 1 game: ARI @ WSH
15 FF league players in wk 1 game: HOU @ BAL
13 FF league players in wk 1 game: GB @ CHI
00 FF league players on team: LV
07 FF league players in wk 1 game: LV @ DEN
14 FF league players in wk 1 game: PHI @ NE
15 FF league players in wk 1 game: MIA @ LAC
12 FF league players in wk 1 game: LAR @ SEA
16 FF league players in wk 1 game: DAL @ NYG
16 FF league players in wk 1 game: BUF @ NYJ
```

Use bash tools for sorted output:

```bash
python3 gotw.py 1 | sort -r
```

Results similar to:

```log
16 FF league players in wk 1 game: DAL @ NYG
16 FF league players in wk 1 game: BUF @ NYJ
16 FF league players in wk 1 game: ARI @ WSH
15 FF league players in wk 1 game: TEN @ NO
15 FF league players in wk 1 game: SF @ PIT
15 FF league players in wk 1 game: MIA @ LAC
15 FF league players in wk 1 game: HOU @ BAL
15 FF league players in wk 1 game: DET @ KC
14 FF league players in wk 1 game: TB @ MIN
14 FF league players in wk 1 game: PHI @ NE
14 FF league players in wk 1 game: JAX @ IND
13 FF league players in wk 1 game: GB @ CHI
13 FF league players in wk 1 game: CIN @ CLE
12 FF league players in wk 1 game: LAR @ SEA
12 FF league players in wk 1 game: CAR @ ATL
07 FF league players in wk 1 game: LV @ DEN
00 FF league players on team: LV
```

## Alternative

There's also a node.js-based [espn-fantasy-football-api](http://espn-fantasy-football-api.s3-website.us-east-2.amazonaws.com/Client.html#setCookies), but I had a hard time getting the [session cookies](http://espn-fantasy-football-api.s3-website.us-east-2.amazonaws.com/Client.html#setCookies) set to access our private league.
