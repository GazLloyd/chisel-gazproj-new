[TOC]

Introduction
===========

Hi, this is a guide to breaking Pokémon Gold/Silver. You will be able to do nearly anything to the games - notably, make any Pokémon shiny and legal for PokéTransporter, so they can be brought into Bank, generation 7 games (except LGP/LGE), HOME, and generation 8 games.

This works for:

* Original English physical copies, assuming your save battery still works/has been replaced
* English 3DS Virtual Console releases
* English emulator ROMs (some emulators may not work as they emulate the RAM slightly differently)

Notably, they do have to be the English versions. Other languages - Japanese, German, whatever - don't work. Additionally, the primary bug we're using is fixed in Crystal version. It has to be Gold or Silver.

We're going to be taking advantage of 2 versions of the coin case glitch, but we'll get to that later.

Shinydex requirements
---------------

If you want to fill up your living shinydex from this, here's the minimum extra you'll need (obviously on a 3DS VC copy), depending on how 'extended completion' you want your dex to be:

* A Pokémon Bank premium subscription - required for PokéTransporter
* A copy of Sun, Moon, Ultra Sun, or Ultra Moon - to be able to use Bank, and to evolve various Alolan variants (X/Y/OR/AS would work for the former - though you can't transfer VC 'mon into generation 6 games)
* A Switch - obviously required to play the Switch releases
* An NSO subscription - required to use HOME
* A Pokémon HOME premium subscription - required to transport from Bank
* A copy of Sword or Shield - required for Galarian Weezing
* Sword/Shield Expansion Pass - required to get Gigantamax forms (I hope you've been collecting Max Mushrooms often!)
* A copy of Legends: Arceus - required for Hisuian evolutions

A number of Pokémon can be evolved in any of the games, including BD/SP, but for the most part evolving things is easier in either Sword/Shield or Legends: Arceus. XP candy is easy to get, evolution items are easy to get (Cram-o-matic or bag retrieval points), and move relearning is trivial. However, feel free to evolve them wherever is most convenient for you.

If you are looking to track a shinydex, feel free to make a copy of [this spreadsheet I made](https://docs.google.com/spreadsheets/d/1pXRKgy2s_ufEyV9oabTMot_sDG1Mj7wzWLLY8C_JzTQ/edit?usp=sharing), with the information you'll need to create the shinies.

Section 0 - Global notes
======

Just a few notes about every section.

* In box names, I have used an underscore `_` to represent a space, just for clarity.
* In box names, all uses of an apostrophe `'` is part of the single-character symbols for `'d 'l 'm 'm 'r 's 't 'v`. You can't use an apostrophe alone.
* I would represent the PK and MN symbols as `@` and `#`, but luckily we don't actually use them. All other symbols are as-is (including things like `é ♂ ♀`).

*ACE* means *Arbitrary Code Execution*, which is the main form of glitch we're doing. An ACE glitch is one where you trick the game into running any code we like - we're taking advantage of the free naming ability of boxes, and the contents of the item storage, and having the game execute those as if they were code.

Section 1 - Basic Progress
=========

This first section is just playing the game normally. The bare minimum you need to do is get to Goldenrod City, though there are reasons to push up to Ecruteak (and get surf access), and maybe even Cianwood.

If you're starting a fresh save, here are some tips:

* Turn off battle animations and use set style, to speed up battles.
* Your name doesn't matter for any glitches, so name yourself whatever. Likewise for your rival's name, and all Pokémon nicknames.
* **Totodile is the best starter by far**
* You don't need to catch anything else or switch at all, just mainline Totodile all the way.
* You probably don't want Mom to save money.
* Up until around level 10, you might as well battle the wild 'mon you encounter, the EXP gained is decent enough. Once you're actually battling trainers, you can start skipping wild 'mon.
* Rage is an excellent move for longer battles, having damage increased every time you get hit. Water Gun is at level 13, so you might be relying on Rage for the first gym.
* Water Gun and Bite are great for stronger physical defences (eg Metapod).
* By the time you get to Goldenrod/Ecruteak you will probably be a Feraligatr. Totodile evolves at level 18, and Croconaw at 30.
* Keep Bite! Replace Scratch with Cut, and later Water Gun with Surf. Bite sweeps Ecruteak gym.
* Grab Berries and equip them - just the regular Berry that heals 10HP is good. Probably won't need to buy potions, but you can if you like.
* Don't forget to grab the bicycle in Goldenrod, near the department store, to speed up movement in general.

It shouldn't take long to get to Goldenrod/Ecruteak.

Here's a gallery of a quick playthrough I did for this guide in an emulator.

$gallery
$img(pkmn/box9_newgame.png, Let's go!)
$img(pkmn/box9_totodile.png, My boy)
$img(pkmn/box9_bellsprout.png, Hey, this saves time later)
$img(pkmn/box9_gym1.png, 1 gym down)
$img(pkmn/box9_croconaw.png, Evolved shortly before the next gym)
$img(pkmn/box9_gym2.png, Second gym!)
$img(pkmn/box9_tm02.png, TM02 Headbutt in Ilex Forest)
$img(pkmn/box9_tm27.png, TM27 Return in Goldenrod Department Store)
$img(pkmn/box9_gym3.png, GG Whitney)
$img(pkmn/box9_feraligatr.png, Feraligatr from the routes up to Ecruteak)
$img(pkmn/box9_vap.png, Hey guys, did you know...)
$img(pkmn/box9_gym4.png, And Ecruteak gym, all done!)
$endgallery

Section 2 - Preparation
============

This part is preparation for the main glitches.

You will need to gather:

* The coin case - pick it up in Goldenrod underground.
* Bellsprout's Pokédex entry - you can encounter it on routes 31 and 32, or pop into Sprout Tower in Violet City and battle any of the trainers there. You don't need to catch it, but you can if you like.
* TM02 (Headbutt) - you can get it for free in Ilex Forest. If you use it, you can buy another in Goldenrod Department Store (5F).
* TM27 (Return) - obtain from the lady that appears in Goldenrod Department Store 5F on Sundays, with a Pokémon with high friendship. See below for boosting friendship quickly.
* A decent amount of money (~10k). You should easily have this much if you beat most trainers on the way and don't overspend on potions. You can beat trainers in the National Park and surfing routes if necessary.
* A Quagsire - you can catch Wooper on route 32 (more common at night); it evolves at level 20.
    * Alternatively, get to Ecruteak, get HM03 from the Kimono sisters and beat the Gym (Bite will likely 1hit everything). Quagsire can be encountered by surfing on route 32 (it likes to flee, so use some great balls right away and savescum if you run out). Given how quickly you progress with an overlevelled Feraligatr, this might be faster than levelling a Wooper! Plus, you get the shortcut back to Violet City & route 32 once you beat Goldenrod Gym.
* A third Pokémon. Doesn't matter what.
* A fourth Pokémon. This one has to be something very low-statted; a low-IV 'mon from route 29 is good. You may need to catch a number of these, so grab a number of balls.
    * Ideally this will be a Hoothoot or Pidgey so you can double up and use it as your Flyer.
    * This is often called the 'slide' Pokémon by the sources I used for this glitch, because the game gets pointed at the stats of this Pokémon and needs to 'slide' off the stats into Quagsire's moves to execute. I'll continue to call this the 'slide' Pokémon.

TM27 and friendship
--------

$img(pkmn/box9_tm27.png, Getting TM27)
Getting TM27 can be awkward. Even if you only ever use Totodile up to Goldenrod, you may not have enough friendship to get the TM (I went all the way to Ecruteak in my second run and I did have enough friendship at that point). If not, you can use the haircut brothers in the Goldenrod underground. Each day, except Monday, one of the brothers will be available to give one of your Pokémon a haircut, boosting friendship. Since waiting a whole real week is dumb, we can reset the time to change days quickly and be done with it very fast.

1. Speak to the brother and get your starter a haircut.
2. Exit the underground and save.
3. Note down your current money, as well as your trainer name and ID (see your trainer card).
4. Reset the game.
5. On the title screen (the one with Lugia/Ho-Oh), press B+down+select at the same time.
6. Say yes to reset the clock
7. Calculate the required password using [this site](http://www.psypokes.com/gsc/timechange.php) or the [utility spreadsheet](https://docs.google.com/spreadsheets/d/1pXRKgy2s_ufEyV9oabTMot_sDG1Mj7wzWLLY8C_JzTQ/edit#gid=1304402925) and enter it.
8. The game will then reset, and upon loading in normally the menu should say the time is ???, and prompt you to enter the time again.
9. You only need to bump the day forward (skipping Monday) for the Haircut brothers, but you can change the time as well if you like.
10. Repeat until Sunday, then check with the TM27 lady in the department store again. If necessary, do another week.

Note that the underground needs to be reloaded - by exiting and entering again - for the brothers to change/allow another haircut, which is why I suggested saving after exiting the underground. If you play through to this point in one sitting, you can initially set your clock to Sunday to allow you to go straight to the TM27 lady, and then do a full week if necessary.

Settings
-----

Before we finish this section, we should do a few settings changes, if you haven't already:

* Set Text Speed to fastest
* Set Menu Account to off (this turns off the description of menu items in the main start menu - if you're reading this guide I think you know what they all mean)
* Change your Pokédex to A to Z mode (press select in the 'dex) - Bellsprout is much closer to the top in this mode
* Move the coin case to the top of key items

Once you have these things, you can proceed to the next section.

Section 3 - Time to glitch
============

Once you have the required things, we can begin the glitch.

Glitch initiation - infinite Rare Candy
------

$img(pkmn/box9_quagmoves.png,Quagsire's moves)
First, teach Quagsire TM27, and move Return it to the first slot (use the 'Moves' option in the Pokémon menu). If Quagsire doesn't have 4 moves at this point, teach it other moves (doesn't matter what) until it does.

Next, give Quagsire TM02. Don't teach, **give** so it is holding it.

Set up your party so that:

* Slot 1 and 2 are anything, doesn't matter at this stage.
* Slot 3 is the slide Pokémon (low-statted like Hoothoot).
* Slot 4 is the Quagsire holding TM02 with Return as its first move.

This is the basic setup that you'll use for all of the glitches of this section. Now we can proceed to do some of them! First off we're going to do a simple one to give us infinite Rare Candies.

Head to your PC and name your Pokémon boxes exactly as follows:

* Box 1: `Ap09é8't5`
* Box 2: `p0a'vAé7't`
* Box 3: `p555'v7'v'd`
* Box 4: `é♂2péD9'l` (that's the male symbol)
* Box 5: `'l5555555`
* Box 6: `555A'lx'd`

Note that `'t` and similar are the single-character symbols that include the apostrophe, found in the lowercase section. You can quickly switch between lower and upper by pressing select.

Glitch activation
------

Once your boxes are named exactly this, follow these steps exactly:

1. Go inside Cherrygrove City Pokémart. (Optional but recommended: save here.)
2. Exit the mart and walk 4 tiles right. You should be stood next to the second tree, the one adjacent to the Pokécenter.
3. Open your menu, then open your Pokédex, then scroll to and open Bellsprout's entry. You don't need to change the page, or even have caught Bellsprout, just have Bellsprout's cry play (which happens when you open the entry).
4. Exit the Pokédex, and without closing your menu, open your pack.
5. Switch pockets to key items. If you were already on key items when you opened the pack, switch away from key items and switch back. **It is important to switch pockets.**
6. 'Use' the coin case.

Upon using the coin case, several things could happen. The correct thing to happen is it tells you the number of coins in your coin case, which is probably 0 (it doesn't matter how many you have). If something else happens, e.g. the game goes directly to a buggy title screen, there is something wrong. Reset the game (to unbug the title screen), then double check your box names. If the boxes are ok, catch a new low-level Pokémon (luckily, route 29 is right there), then try again from step 1.

You may take a number of low level 'mon until you get one that works.

Once you have one that works, and the coin case doesn't reset the game, continue:

<ol start=7>
<li>Exit your pack. You may need to mash B, as menus tend to get much less responsive during this section.</li>
<li>Second check: your player sprite should have disappeared from the map.</li>
<li>Save the game. Again, mash down to get to save, and A to save, if necessary.</li>
<li>Once saved, reset the game.</li>
</ol>

Once loaded back in, check your balls pocket of your pack - the first slot should now be []5 x Rare candy. This is 255, but because the rare candy is in the balls pocket, it is actually infinite! The number will never decrease. You can use as many as you like to level up, or sell as many as you like to make some money.

Now that you have a low levelled 'mon that works for this glitch, it will **always** work with that 'mon. Make sure you don't accidentally level it up or release it. Once you get back to Goldenrod (we'll get Fly access shortly, don't worry), consider renaming it so you remember.

$gallery
$img(pkmn/box9_mart.png,Step 1: Inside the mart - save here!)
$img(pkmn/box9_treebymart.png,Step 2: 4 tiles right of the mart, by the tree)
$img(pkmn/box9_bellsprout_dex.png,Step 3: Bellsprout's dex entry)
$img(pkmn/box9_nosprite.png,Success! We have no sprite, the glitch worked)
$img(pkmn/box9_inf_rc.png,And here we have 255x Rare Candies in the Balls pocket)
$img(pkmn/box9_broken_title.png,A broken title screen - something was wrong, reset and try again)
$endgallery

All TMs
------

$img(pkmn/box9_umlaut.png,BOX14 with ä)
The next glitch uses the same set up and execution, just with some new box names.

This one simply changes one of the characters in the box 14 name to be `ä`, which is not a character we can usually type into a box name. This is needed for the next 2 glitches.

* Box 1 : `Ap0w'vA55 `
* Box 2 : `é'm2p'v7'v'd`
* Box 3 : `éA355555`
* Box 4-12: `55555555`
* Box 13: `5555péD9`
* Box 14: `'l'lA'lx'd55`

After doing the glitch process (exit Cherrygrove Mart, 4  steps right, Bellsprout's cry, switch pockets, coin case, save, reset). Check that the box has the `ä` character.

$img(pkmn/box9_255tms.png,255 of every TM)Next, we're going to get 255 of every TM. Set your box names to:

* Box 1: `Ap'vCé225`
* Box 2: `'vj'vué125`
* Box 3: `'v.é52p'v9`
* Box 4: `é42pé625`
* Box 5: `'vué82'v 5`
* Box 6: `é72'v:é92`
* Box 7: `0955't5`
* Box 8-12: `55555555`
* Box 13, 14: Same as before, don't change them.

After the process, check you have all the TMs.

Creating items
----

Now, typing in all of these box names is getting quite tedious right? We are going to transform items in our pack into the things we need to enable a much easier way to do things. This will be the last time we rename a lot of boxes. First, name your boxes:

* Box 1: `A4A'téy't5`
* Box 2-12: `55555555`
* Box 13, 14: Same as before, don't change them.

This box name will transform the first item in the items pocket into something else, based on the number of TM03 in your pack. We'll be selling/tossing a number of them to spawn specific things.

I suggest doing the following order. If you accidentally get rid of too many, you'll need to re-do the above code to get 255 of each TM again. This order is designed to not have to do that.

You can get some of the items below in other ways. Notably, Super Repels can be bought in Cianwood City - you'll have to progress normally (though quickly if you rare candy your starter). Once you're there, you might as well beat the gym to allow use of Fly to get back to Cherrygrove. Feel free to skip items you can buy easily elsewhere.

The process for this glitch is as follows:

1. Buy potions or something to go into the items pocket in the required number
2. Move it to slot 1 (press select)
3. Sell/toss the number of TM03 to get the number required
4. Perform the glitch process from above (exit Cherrygrove Mart, 4 steps right, Bellsprout's cry, switch pockets, coin case, save, reset)
5. Repeat with another number of TM03

You can deposit extra items into your PC if you need space; sell some Rare Candy if you need money. You will need to get 194 Dire Hits and 201 Super Repels, so buy that many, or repeat the glitch to get additional stacks.

<div id="box9-tm03-list" markdown="1">
| **Item spawned** | **Quantity needed** | **TM03 needed** | **Throw out this many TM03** | **Alternate Source**         |
|------------------|---------------------|-----------------|------------------------------|------------------------------|
| Flower mail      | 51                  | 158             | 97                           | Goldenrod Department Store   |
| Berry Juice      | 1                   | 139             | 19                           | Shuckle                      |
| Pass             | 1                   | 134             | 5                            | Saffron City (postgame)      |
| Stardust         | 1                   | 131             | 3                            | Rarely held by wild Staryu   |
| Ether            | 3                   | 63              | 68                           | find it lol                  |
| X Speed          | 1                   | 52              | 11                           | Goldenrod Department Store   |
| Dire Hit         | 99                  | 44              | 8                            | Goldenrod Department Store   |
| Dire Hit         | 95                  | 44              | 0                            | Goldenrod Department Store   |
| Super Repel      | 99                  | 42              | 2                            | Cianwood Mart                |
| Super Repel      | 99                  | 42              | 0                            | Cianwood Mart                |
| Super Repel      | 3                   | 42              | 0                            | Cianwood Mart                |
| Full Heal        | 18                  | 38              | 4                            | Goldenrod Department Store   |
| X Accuracy       | 7                   | 33              | 5                            | Goldenrod Department Store   |
| Protein          | 1                   | 27              | 6                            | find it lol                  |
| Potion           | 46                  | 18              | 9                            | Cherrygrove Mart (or others) |
| Poké Ball        | 94                  | 5               | 13                           | Cherrygrove Mart (or others) |
</div>
Once you've gotten all of these items, we're ready to proceed.

Gallery
-----

$gallery
$img(pkmn/box9_tm03_158.png,158xTM03 = Flower Mail)
$img(pkmn/box9_tm03_139.png,139xTM03 = Berry Juice)
$img(pkmn/box9_tm03_134.png,134xTM03 = Pass)
$img(pkmn/box9_tm03_131.png,131xTM03 = Stardust)
$img(pkmn/box9_tm03_63.png,63xTM03 = Ether; now we can see the number correctly)
$endgallery

Section 4 - BOX9
============

Item Storage setup
-----

Now, you will need to set up your PC item storage to be precisely this:

    [Any Item] x[Any Amount]
    [Any Item] x[Any Amount]
    X Accuracy x7
    TM26 (Earthquake) x1
    [Any Item] x[Any Amount]
    Super Repel x94
    Stardust x1
    [Any Item] x[Any Amount]
    Dire Hit x87
    Super Repel x55
    Ether x3
    Poke Ball x94
    Berry Juice x1 
    [Any Item] x[Any Amount]
    Dire Hit x95
    Super Repel x3
    Pass (x1)
    [Any Item] x[Any Amount]
    Potion x46
    HM03 (Surf) (x1)
    X Speed x1
    Full Heal x18
    Flower Mail x51
    TM06 (Toxic) x1
    [Any Item] x[Any Amount]
    TM41 (ThunderPunch) x[Any Amount]

You may notice the multiple stacks of some items (Dire Hit and Super Repel). You will need to deposit 99 Dire Hits, then deposit 95, then withdraw 12 from the first stack so there are 87. Repeat with Super Repels: 99, 99, 3, withdraw 5 and 44.

Remember you can use select to move items around, so you needn't withdraw things you deposited for space earlier, if they are on the list.

The [any item]s can be anything that isn't in the list - buy some additional X items, mails, or just use some of the TMs you have from the previous glitch.

Withdraw/toss anything else that isn't on the list. Make sure to keep the Protein!

New setup - 255 Master Balls
----

$img(pkmn/box9_quagmoves2.png,Quagsire's new moves)Now, teach TM35 (Sleep Talk) to Quagsire, and make that the first move slot. I kept Return, but you're probably good to overwrite it if you like (you should have 255 TM27s anyway). Give Quagsire the Protein to hold; you may need to throw out a TM02 to be able to take it from Quagsire.

Now to make sure that this is working, we're going to change the first item in the balls pocket to Master Balls. Make sure to put something else at the top of the balls pocket if you haven't moved the rare candies away, as this would overwrite them (though easily fixed).

Now just rename the 9th box in your Pokémon storage to `'v989AB`. The other boxes don't matter - I personally changed the name of boxes 1-8 and 10-12 back to BOX#, leaving 13-14 with the names just in case I wanted to do the earlier glitches again.

Now perform the same glitch process again. Just to reiterate:

1. Set up your party so that slot 1 and 2 are anything, slot 3 is the slide Pokémon (the same one from before will work), and slot 4 is Quagsire holding Protein with Sleep Talk as its first move.
1. Enter Cherrygrove Pokémart (a good point to save, as before)
2. Leave the mart, walk 4 steps right (next to the second tree)
3. Open the Pokédex, listen to Bellsprout's cry
4. Close 'dex, open the pack, change pockets (still important to change pockets)
5. Use the coin case

Notes:

* Make sure to (enter and) exit the mart each time.
* If you mess up and listen to the wrong cry, enter the party or other menu, don't switch pockets, use the wrong item or whatever, restart the process (re-enter mart). Don't worry, it is easy to accidentally 'typo' and go into the wrong menu, I did it plenty.
* You don't need to save & reset each time.
* If your game does something other than display the number of coins in your case (e.g. glitched text, glitched sprites, resets to title screen, etc), something is wrong. Also applies if the glitch displays the number of coins correctly, but the effect is wrong (e.g. balls slot 1 is not master ball). Reset without saving and try again, and/or see the below steps:
    1. Make sure your party setup is correct
    2. Check your box 9 name is correct
    3. Check your item storage is exactly as the list above
    4. Catch a new slide 'mon, though this shouldn't be a problem if it worked for the above previous section's glitches.

$img(pkmn/box9_masterball.png,Master ball now in slot 1)The glitch is now complete. Check your balls pocket - slot 1 should now be Master Ball (with the same quantity of whatever was there before).

This version is much more stable, and will not cause the same side effects as the earlier version - you don't need to save and reset after every use, so you can do many codes in a row.

$img(pkmn/box9_masterball255.png,255xMaster ball)Change the box 9 name to `'v999_A` and repeat the glitch process to set the quantity of balls slot 1 to 255.

Once it works, this is the basic process for everything we're doing from now: change the box name, do the glitch process, repeat.

Section 4.5 - basic explanation
=========
This glitch is highly targetted RAM address editing - each use edits one RAM address to whatever value. In short:

* The coin case glitch (using the coin case right after listening to Bellsprout's cry) makes the game start executing your party as if it is code
* It starts off in the stats of the third slot. Having the stats low is equivalent to having no-ops (no operations, code that does nothing), so the game 'slides' through until it reaches party slot 4.
* The specific setup of Quagsire, holding Protein, knowing Sleep Talk as its first move makes the game jump to elsewhere in RAM to execute code - to your PC item storage.
* The complicated setup of items in your item storage makes the game take the name of the 9th box of your Pokémon storage as a RAM address and new value for that address.
* Then it resumes normal play.

RAM is addressed with 2 bytes, and contains 1 byte. This is generally represented as hexadecimal characters, for example D5FD is the RAM address of the item in slot 1 of your balls pocket. We set that to the internal ID of Master Balls, which is 01. The box 9 glitch just wants those as one 6-character string, so its D5FD01.

However, the hexadecimal characters are not what we name the box - we need to turn them into the actual characters, based on the internal ID of the characters. The glitch doesn't see the characters `'v9`, it sees the internal IDs of these, smushed together - which is D5.

Since character IDs are mostly fairly high - generally starting at 0x74, there can't be a simple 1:1 hex digit to box character mapping, nor a 1:1 byte to box character mapping, so we use two box characters to be 1 byte. It uses the fact that the address will wrap around - numbers above 255 wrap back around to 0. E.g. `A` is ID 128, and `B` is 129. `AB => 128+129 = 257 => 1`, which is the ID of the Master Ball.

The below table can be used to lookup the conversion between hexadecimal and box characters.

<div id="box9-hexconvert-table" markdown="1">
|    | -0  | -1  | -2  | -3  | -4  | -5  | -6  | -7  | -8  | -9  | -A  | -B  | -C  | -D  | -E  | -F  |
|----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| 0- | AA  | AB  | AC  | AD  | AE  | AF  | AG  | AH  | AI  | AJ  | AK  | AL  | AM  | AN  | AO  | AP  |
| 1- | AQ  | AR  | AS  | AT  | AU  | AV  | AW  | AX  | AY  | AZ  | BZ  | CZ  | DZ  | EZ  | FZ  | GZ  |
| 2- | HZ  | IZ  | JZ  | KZ  | LZ  | MZ  | NZ  | OZ  | PZ  | QZ  | RZ  | SZ  | TZ  | UZ  | VZ  | WZ  |
| 3- | XZ  | YZ  | ZZ  | aT  | aU  | aV  | aW  | aX  | aY  | aZ  | bZ  | cZ  | dZ  | eZ  | fZ  | gZ  |
| 4- | hZ  | iZ  | jZ  | kZ  | lZ  | mZ  | nZ  | oZ  | pZ  | qZ  | rZ  | sZ  | tZ  | uZ  | vZ  | wZ  |
| 5- | xZ  | yZ  | zZ  | ta  | ua  | va  | wa  | xa  | ya  | za  | zb  | zc  | zd  | ze  | zf  | zg  |
| 6- | zh  | zi  | zj  | zk  | zl  | zm  | zn  | zo  | zp  | zq  | zr  | zs  | zt  | zu  | zv  | zw  |
| 7- | zx  | zy  | zz  | ?N  | ?O  | ?P  | ?Q  | ?R  | ?S  | ?T  | ?U  | ?V  | ?W  | ?X  | ?Y  | ?Z  |
| 8- | ?(  | ?)  | ?:  | ?;  | ?[  | ?]  | ?a  | ?b  | ?c  | ?d  | ?e  | ?f  | ?g  | ?h  | ?i  | ?j  |
| 9- | ?k  | ?l  | ?m  | ?n  | ?o  | ?p  | ?q  | ?r  | ?s  | ?t  | ?u  | ?v  | ?w  | ?x  | ?y  | ?z  |
| A- | 9b  | 9c  | 9d  | 9e  | 9f  | 9g  | 9h  | 9i  | 9j  | 9k  | 9l  | 9m  | 9n  | 9o  | 9p  | 9q  |
| B- | 9r  | 9s  | 9t  | 9u  | 9v  | 9w  | 9x  | 9y  | 9z  | 'r? | 's? | 't? | 'v? | 'v! | 'v. | 'v& |
| C- | 'vé | 'm♂ | 'r♂ | 's♂ | 't♂ | 'v♂ | 'd0 | 'd1 | 'd2 | 'd3 | 'd4 | 'd5 | 'd6 | 'd7 | 'd8 | 'd9 |
| D- | 'l9 | 'm9 | 'r9 | 's9 | 't9 | 'v9 | !♂  | .♂  | &♂  | é♂  | !/  | ./  | &/  | é/  | .0  | .1  |
| E- | .2  | .3  | .4  | .5  | .6  | .7  | .8  | .9  | &9  | /0  | /1  | /2  | 00  | 01  | 02  | 03  |
| F- | 04  | 05  | 06  | 07  | 08  | 09  | 19  | 29  | 39  | 49  | 59  | 69  | 79  | 89  | 99  | _A  |
</div>

You can look up the RAM addresses [here](https://datacrystal.romhacking.net/wiki/Pok%c3%a9mon_Gold_and_Silver:RAM_map#Pokemon_1_Settings), and there is a map of character, Pokémon species, moves, and items to their IDs in decimal and hexadecimal [here](https://glitchcity.wiki/The_Big_HEX_List#Coin_Case_box_name_character_version_by_Sanqui).

So, for our Master Ball examples:

* Ball slot 1 is RAM address D5FD (from the RAM map)
* Master Ball ID is 01 (from the ID map)
* Thus we need to translate D5FD01
* D5: `'v9`; FD: `89`, 01: `AB`
* So our box name is `'v989AB`
* Ball slot 1 quantity is RAM address D5FE
* Quantity we want is 255, or FF in hex
* D5: `'v9`, FE: `99`, FF: `_A`
* So our box name is `'v999_A`

I made this calculator to easily translate a RAM address+value in hex into box names [here](https://chisel.weirdgloop.org/gazproj/pkmn/gs), if you've had enough of manually translating the characters.

Now we can do almost anything to the game!

Section 5 - Some utility codes
==========

$img(pkmn/box9_badges.png,All Johto badges)
This is a short section with a few utility codes to unlock the rest of the game quickly. Just perform the process with each code as the name of box 9. Just for clarity, I have added a space between the address and value.

<div id="box9-utility-codes" markdown="1">
| Use                   | RAM edits | BOX9 names  |
|-----------------------|-----------|-------------|
| Unlock all fly points | `D9EE FF`<br />`D9EF FF`<br />`D9F0 FF`<br />`D9F1 FF`   | `é♂02_A`<br />`é♂03_A`<br />`é♂04_A`<br />`é♂05_A` |
| Johto badges          | `D57C FF`   | `'v9?W_A`     |
| Kanto badges          | `D57D FF`   | `'v9?X_A`     |
</div>

$img(pkmn/box9_flylocs.png,All fly locations, so I can fly to Silver Cave)
After this, you should have all 16 badges, and be able to fly between all points. If you like, you can get into Kanto by flying to Mt. Silver and walking east, though if you fly to a Kanto city, you'll have to repair the power plant (speak to manager there, get the part from inside Cerulean gym, speak to him again) and get a real Pass (speak to copycat girl in Saffron, speak to guy in Pokéfan club in Vermillion, speak to copycat again) to take the monorail back to Johto. This guide doesn't require anything from Kanto, so you don't even need to get the badges.

Section 6 - How to make shinies
=======

Now the real reason you're here - we're gonna make some shiny Pokémon!

Shininess
----

In generation 2, the shininess of Pokémon is determined by their IVs - as is gender and Unown letter (we'll come back to that later). A shiny has a Defense, Special, and Speed IV of 10, and an Attack IV of 2, 3, 6, 7, 10, 11, 14, or 15. Since IVs (in gen2) can be 0 to 15, and everything is equally likely to occur, that means the natural shiny chance is `1/16 * 1/16 * 1/16 * 8/16 = 1/8192`. (The red Gyarados at the Lake of Rage has 14 Attack and 10 other IVs.)

But, we know how to edit the RAM. And would you look at that, the Pokémon IVs are there. Addresses DA3F and DA40 for party slot 1.

Making a shiny
----

$img(pkmn/box9_shiny_hoothoot.png,Shiny Hoothoot!)
So let's test! You probably still have that garbage extra 3rd 'mon we caught earlier, or some other weak 'mons that didn't work for the glitches. Put one of them as slot 1 of your party. Slot 2 continues to not matter, 3 should be the slide, and 4 should be Quagsire, as usual.

Name your box 9 `!/gZ59`. This is RAM edit `DA3F FA`. DA3F is Attack and Defence IV, which we are setting to 15 (F) and 10 (A) respectively. Perform the glitch process (you probably won't notice any difference yet). Then, name your box `!/hZ9l` - RAM edit `DA40 AA`, to set Speed and Special to 10 (A) respectively. Perform the process - your slot 1 Pokémon should now be shiny (also, if it was female, it'll be male now)!

This is the basic process for changing a Pokémon you've caught yourself to be shiny. And since you have (or can make) 255 Master Balls, you're free to just go wild: catch and shinify anything you like.

Transforming species
------

$img(pkmn/box9_not_hoothoot.png,That's not a Hoothoot!)
Buuuut... what about rare stuff? Or stuff that just is not present in the wild at all?

You might have noticed that a little above the IVs in the RAM map, we have the Pokémon species at DA2A. How about we change that?

With the same Pokémon as slot 1 (or a different one if you like, doesn't matter), change box 9 name to `!/RZ/0` and do the usual process. If you check on your 'mon now...

$img(pkmn/box9_real_porygon2.png,Now there's a real Porygon2)
Huh, nothing changed. Well, how about we go battle with it.

Oh hey! The Pokémon is now using Porygon2's sprite! Yep, this code changes the Pokémon in slot 1 of your party to be number 233 (hex E9), which is Porygon2. However, it is in a weird transitory state where it kinda also is not changed, as you see in the normal check-stats menu.

To cement the species change, deposit the 'mon in the Daycare (just south of Goldenrod City) and withdraw it. Bam! It is now the 'correct' species - that is, Porygon2 (if your sound is up, it'll make the original cry when deposited, and Porygon2's cry when withdrawn). Since we only edited the species, if you used the shiny one we made before, it'll still be shiny.

The 'transitory' state Pokémon are stable - you can move them around in your party, deposit them in the PC, go into battle, heal at a center, etc., without them reverting to the original species. The main issue is that PokéTransporter will refuse to move them out to Bank.

PokéTransporter and legality
----

Speaking of PokéTransporter, it will also refuse to move a 'mon that has an illegal moveset or level. It will likely refuse the Porygon2 if you made it from a Hoothoot or Sentret, as they will probably know Scratch, which Porygon and Porygon2 cannot learn. Or, if we made a Feraligatr from a level 4 Hoothoot, that would also be illegal as Feraligatr evolves at level 30; also illegal would be a level 4 Mewtwo, as Mewtwo only appears in the wild at level 70.

You can use TMs to teach it moves it is allowed to learn and overwrite illegal moves, or go to Blackthorn City and use the move deleter to remove illegal moves. You can level up the 'mon using Rare Candies (which will likely teach it moves too), or use box 9 name `!/qZxZ` to set it to level 80 (an always-safe level) (you will need to use a rare candy to make the level 'real' - note that daycaring it will revert the level change).

Not a legality problem, but the Pokémon's nickname will be the original species' name - you can change this at the name rater in Goldenrod.

This is kind of a tedious process, but we can significantly speed it up to do a lot of shinies.

Section 7 - Shiny prep
========

Now, rather than go through that process of shinifying, changing species, levelling, adjusting moves, and renaming every Pokémon, we can do this to one Pokémon then clone it a bunch. 

Cloning
----

Cloning in Gold and Silver is actually extremely easy. Let's do it to a test 'mon first so you get the process down, then we can prepare and clone the real thing.

Here's how you clone a 'mon:

1. Save the game normally
2. Open your PC Pokémon storage (any box, as long as there's space)
3. Deposit the Pokémon to clone into the box
4. Go into Change Box and initiate changing boxes (to any other box)
5. It will ask you to save. Say yes.
6. It'll ask you to overwrite. Say yes, and be ready.
7. About 3 seconds after saying yes to overwrite - coincedentally, right as the word `POWER.` finishes appearing - reset the game. In the VC releases, you just have to tap the bottom screen at the appropriate time as this will suspend the game, then you can hit Reset and Yes at your leisure. In emulators, get familiar with your 'reset gameboy' hotkey. For physical releases, probably turn off the power?
8. Once reset and loaded back in, you should find that the Pokémon is still in your party, and also is deposited in the box. Clone successful!

If you only have one of the 'mon, you hit suspend/reset at the wrong time - in your party only, too early; in the box only, too late. This glitch is fairly lenient, with a good 0.25-0.5 seconds leeway to reset and be successful - it is far from frame perfect, but you can still tap a little late and just deposit the 'mon.

This is pretty safe; you're extremely unlikely to lose the 'mon. This does work in Crystal too, but the timing is a little different and much less lenient, and if you mess up you're way more likely to lose the 'mon - another benefit to G/S.

You can clone up to 5 Pokémon per cycle, since you need to keep 1 in your party.

Making a base-shinymon
-----

$img(pkmn/box9_zig_ready.png,A base-shinymon ready for cloning)
Once you've successfully cloned a garbage 'mon, now it is time to start prepping what I'll call our *base-shinymon*. I decided to use my Feraligatr, since it was already level 80 at this point from Rare Candies. I cloned it once to keep the original version of the starter, and began working on it.

1. I renamed it to something I wouldn't mind being the name for a lot of shiny 'mon. My Trainer name was Gaz, and I named my Totodile Zag, so I called the base-shinymon Zig. If you want to name your resulting shinies as their species name, you'll just have to do that for every 'mon - there just isn't a shortcut for that.
2. I used the shiny box names to make Zig shiny (`!/gZ59` and `!/hZ9l`).
3. As mentioned, my Feraligatr was already level 80, but here is a good time to level it to about that. It is worth going above level 70, as the experience curves of some species will alter the level of the 'mon. Your legendaries will end up at level 74 if you start with a level 80 Feraligatr, which is still safe - if you use a level 70 Feraligatr, you'll need to level some legendaries to make them legal.
4. Teach the base-shinymon TM06 (Toxic). There are only 8 'mon that cannot learn Toxic in generation 2, which I'll point out later.
5. Delete all of the other moves in Blackthorn, so it knows only Toxic.

This is now the complete base-shinymon - a high level so it is always legal, already shiny, has a legal moveset for the majority of 'mon, and has an OK nickname. All I need to do to it is change the species (then daycare it to cement the species), and we're good to go!

Cloning base-shinymon
-----

$img(pkmn/box9_ready_to_clone.png,6 Zigs for easy mass cloning)
Now clone the base-shinymon a bunch of times. Exactly how many you want to do depends on you. I personally:

1. Cloned until I had 6. You only need 5, but 6 allows you to just mash A to deposit instead of having to scroll past the first in your party.
2. Cloned 5 into box 14, which was where I was also storing my original starter. This is just a safety precaution, so I had some stored away safely in case I accidentally PokéTransporter'd all of them.
3. Cloned 7 full boxes of them, giving me 140 to work with.
4. If/when I ran low I cloned another box or two.

$img(pkmn/box9_full_box_of_zig.png,A box of ready base-shinymon)
To get every shiny out of this as you possibly can, including females with gender differences and future forms/evolutions, you will need:

* 251 for a the full Pokédex
* +41 females (50%) - change the Attack IV to 7 with `!/gZ?U`, then clone that
* +2 females (25%) - change Attack IV to 3 with `!/gZbZ`
* +17 for future evolutions (mostly generation 4 stuff)
* +4 females (50%) for future evolutions
* +3 for Alolan evolutions
* +1 for Galarian evolutions
* +4 for Hisuian evolutions
* +12 for Gigantamax forms
* +2 females (50%) for Gigantamax forms

A total of 337. You will need to clone multiple times, as you can't store that many in the generation 2 games.

There are 3 females with gender differences (Venusaur, Eevee, Meganium - 2 of these have gigantax forms too), that you cannot get using this glitch. See the section below on making females for details.

Bulk species transformation process
-------

Now for the main operations (making the species), I did as follows:

1. Withdraw 4 base-shinymon, Quagsire, and the low-level 'mon.
2. Setup party order (2 base-shinymon, Hoothoot, Quagsire, another 2 base-shinymon). (After the first time, you can do this after exiting the daycare, then fly back to Cherrygrove from the same menu.)
3. Perform box 9 name glitch to change species of all four base-shinymon. (see below)
4. Fly to Goldenrod. Daycare all 4 to cement species.
5. Deposit all 4 into box 1.
5. Repeat 1-5 until box 1 is full.
6. Save, close G/S, open PokéTransporter, send box 1 into Bank.
7. Close PokéTransporter, open Bank, move transport box into Bank boxes.
8. Save and quit Bank, open and load back into G/S.
9. Repeat.

My suggestion is to daycare a block of 4 each time. You could deposit things into a box, then withdraw more base-shinymons, without daycare-ing, but I found it easy to lose track of what I had changed and what I hadn't. 4 was enough to make OK progress each round, but also easy to keep track of, and quick enough to do without getting distracted mid-group and just forgetting everything.

When performing the species changing process, the following worked for me to keep track mentally:

1. Do the process for whatever your party order starts as (after putting Hoothoot and Quagsire in the right place). So now Slot 1 is in the transitory state.
2. Swap Slot 1 and Slot 2, then do the process. Slot 1 and 2 are now transitory.
3. Swap 1 and 6, and 2 and 5 (or 1-5 and 2-6). I like to think of it as 'outsides' (1-6) and insides (2-5) (you could use odds/evens for the other way). The end goal is to swap the 1+2 block with the 5+6 block, so that 5+6 are the transitories.
4. Do the process (1,5,6 transitory), swap 1 and 2, then do the process again. Now all 4 are transitory, ready to daycare or deposit.

Alternatively...
-----

An alternative method could be:

1. Clone until you have 4 in your party.
1. Clone a couple for safety.
2. Use box 9 to alter the species/etc of each. Daycare to cement changes.
3. Clone the altered 'mons into box 1.
4. Repeat from step 2; PokéTransporter out when box 1 is full.

This method is basically just repeatedly cloning your party into box 1 each round, instead of doing a bulk cloning session upfront and deposit/withdrawing stuff each round. It should be safe to do with transitories, but I didn't check.

Gallery
-----

<div class="img-autosize" markdown="1">
$gallery
$img(pkmn/box9_bank.jpg,Shinies after being transported into Bank)
$img(pkmn/box9_home.jpg,Box of the moved-over ones in HOME)
$img(pkmn/box9_home_zig.jpg,Base-shinymon in HOME app!)
$img(pkmn/box9_home_mobile.jpg,Zigs in HOME app)
$img(pkmn/box9_evo_ambipom.jpg,Ambipom evolved in PLA)
$img(pkmn/box9_evo_weavile.jpg,Weavile evolved in PLA)
$endgallery
</div>


Section 8 - Special Pokémon
=========

Female Pokémon
-----

In generation 2, gender is determined entirely by Attack IV. The female chance is multiplied by 16, and if the Attack IV is less than this, the 'mon is female. So, in a 1:1 (50% m, 50% f) species, 0-7 Attack IV is female, 8-15 is male.

Thus, for various ratios, we need to use these box 9 name to adjust the Attack IVs to get shiny females (ratios are m:f):

* 0:1 - 100% female - no change (can use `!/gZ59`)
* 1:7 - 87.5% female - there are no generation 1-2 species with this ratio
* 1:3 - 75% female - `!/gZ's?` - there are no current species with gender differences of this ratio from generation 1-2 (Attack IV = 11)
* 1:1 - 50% female - `!/gZ?U` - majority of species with gender differences are this ratio (Attack IV = 7)
* 3:1 - 25% female - `!/gZbZ` - gender differences: Kadabra and Alakazam (Attack IV = 3)
* 7:1 - 12.5% female - Impossible - gender differences: Venusaur, Eevee, Meganium
* 1:0 - 0% female - no change (can use `!/gZ59`)

Notably, 7:1 ratio (87.5% male, 12.5% female) are impossible to be both female and shiny in generation 2. As mentioned above, Attack IVs for shininess are 2,3,6,7,10,11,14,15. Females in a 7:1 species females can only have an Attack IV of 0 or 1. Thus, they cannot be both. This affects: all 6 starter lines, all 3 fossil lines, Eevee and -lutions, Snorlax, and Togepi line.

If you're planning on getting a bunch of females, consider adjusting your base-shinymon to be of the correct IVs then clone the new IV 'mon a bunch.

Unown
-----

I mentioned above that Unown form is also based on IVs. This is a bit more complicated than gender, but I will summarise it here.

Unown takes the center two bits (a "nibble") of the Attack, Defence, Speed, Special IVs, sticks them together (in that order) to get an 8-bit number (0-255). This is then integer divided by 10 to get a number 0-25, which is that Unown's letter (where 0=A, 25=Z).

Because shininess fixes IVs, bits of the number have to be `XX010101`, (10 in binary is `1010`, so the center two bits are `01`). Additionally, the Attack bits can only be `01` or `11` (2,3,10,11 center bits are `01`, and 6,7,14,15 are `11`). So, the letter can be `01010101 = 85 => 8 = I`; or `11010101 = 213 => 21 = V`. Only Unown I or Unown V can be shiny, a fun coincidence!

Box 9 name `!/gZ59` will get you an Unown V, and `!/gZ's?` will get you Unown I.

Nontoxic Pokémon
-----

8 species of Pokémon cannot learn Toxic and will be rejected by PokéTransporter for being illegal if they do know it. They are:

* \#10 Caterpie
* \#11 Metapod
* \#13 Weedle
* \#14 Kakuna
* \#129 Magikarp
* \#132 Ditto
* \#201 Unown
* \#202 Wobbuffet

**Option 1: Just catch them**

For these 'mon, you have a couple of options. The easiest for some of them is to just go catch one normally then shinify it with the box 9 names from above.

* In Gold, Caterpie and Metapod are on routes 30 and 31, and in Ilex Forest. In Silver, they are only in the Bug-Catching Contest in the National Park.
* In Silver, Weedle and Kakuna are on routes 30 and 31, and in Ilex Forest. In Gold, they are only in the Bug-Catching Contest in the National Park.
* Magikarp are on basically every route with water, with the Old Rod (get it from the fisher in the PokéCenter on route 32).
* Ditto are on routes 34 and 35 with a very low encounter rate (5% and 4%)
* Unown are in the Ruins of Alph after solving at least one of the puzzles
* Wobbuffet are in the Dark Cave, route 45 side, with a low encounter rate (15%)

**Option 2: Breeding**

You could use box 9 to make one/two of the species, then breed it and hatch the egg, then shinify the hatched 'mon (this is too tedious, for me).

**Option 3: Evolve**

For Metapod and Kakuna, Caterpie and Weedle can be evolved and it will learn Harden, then you can delete Toxic.

**Option 4: BOX9 to replace moves**

You could use box 9 to change the first move to be a legal one. Here are some codes for moves (move 1 of Pokémon 1 is address DA2C):

* Tackle (Caterpie, Metapod, Magikarp): `!/TZIZ` (DA2C 21)
* Poison Sting (Weedle, Kakuna): `!/TZPZ` (DA2C 28)
* String Shot (Caterpie, Metapod, Weedle, Kakuna): `!/TZyZ` (DA2C 51)
* Transform (Ditto): `!/TZ?k` (DA2C 90)
* Hidden Power (Unown): `!/TZ01` (DA2C ED)
* Counter (Wobbuffet): `!/TZlZ` (DA2C 44)

**Option 5: Level 0**

And finally, you could change the Pokémon's level to 0 with box 9 (`!/qZAA`), then use a Rare Candy to level to 1, which will cause the 'mon to learn its default moves. Then Rare Candy or box 9 (`!/qZwZ` for level 79) to level back up if you like. After changing level with box 9, you should Rare Candy to cement the level (daycare-ing it will revert the box 9 level change).

Use whichever you feel is easier - I used several of the methods.

Mew
-----

Mew is special in that it can only be PokéTransport'd if it has the ID and OT of the event Mew. Other IDs and OTs are not allowed at all.

The ID needed is 22796. You can set this with the box 9 names `!/XZza` and `!/YZAM` (22796 in hex is 590C. DA30 and DA31 are the addresses for the ID, so we use DA3059 and DA310C as successive box names).

The OT needed is GF. We can set this with `./rZ?a`, `./sZ?]`, and `./tZxZ`. (DB4A through DB54 are the addresses for OT, one address for each character. We need set it to the ID number in hex of G (86), F (85), and a string terminator (7F).)

If necessary, you may need to write over the rest of the characters of your name - I tested in an emulator with a long name and it does appear to not need this, but I couldn't test PokéTransporting the Mew. If it fails, these are the box names for the rest of the characters (space between each): `./uZxZ ./vZxZ ./wZxZ ./xZxZ ./yZxZ ./zZxZ ./taxZ ./uaxZ`, use as many as you need.

Celebi can be transferred normally, as it is not given directly by the event, but caught by the player (so has the player's ID and OT, and is legal with that).

$gallery
$img(pkmn/box9_mew_1.png,A Zig made into a Mew and daycare'd)
$img(pkmn/box9_mew_2.png,ID changed)
$img(pkmn/box9_mew_3.png,RIP GilvaSunner)
$img(pkmn/box9_mew_4.png,I too LV my GF)
$img(pkmn/box9_mew_5.png,And this Mew should now be legal to PokéTransport)
$endgallery

Levels
-----

Most 'mon can be transferred at level 5 if unevolved (since that's the level eggs hatch at), or at the evolution level for the species if it is evolved. Here are some exceptions (they are all legendaries):

* Articuno, Zapdos, Moltres: 50 (encounter level in RBY)
* Mewtwo: 70 (encounter level in RBY)
* Raikou, Entei, Suicune: 40 (encounter level)
* Lugia: 40 (encounter level in Silver)
* Ho-Oh: 40 (encounter level in Gold)
* Celebi: 30 (encounter level in the Crystal event)

As such, if you followed what I did and used your starter as the base-shinymon, and set it to level 80, the XP curve change from that to a legendary puts the legendary at level 74, which is also always legal.

Conclusion
======

Hey, thanks for reading. Let me know if any part of this needs adjustment. Happy glitching!

-Gaz

Extra Resources
-----

These are linked throughout, but here is a compilation of them anyway.

* [My utility spreadsheet](https://docs.google.com/spreadsheets/d/1pXRKgy2s_ufEyV9oabTMot_sDG1Mj7wzWLLY8C_JzTQ/edit?usp=sharing), which you should make a copy of and use it to track your progress
* [IDs of characters, items, Pokémon, and moves in hex](https://glitchcity.wiki/The_Big_HEX_List#Coin_Case_box_name_character_version_by_Sanqui)
* [RAM map](https://datacrystal.romhacking.net/wiki/Pok%c3%a9mon_Gold_and_Silver:RAM_map)
* [GS time change password generator](http://www.psypokes.com/gsc/timechange.php)

References and credits
----

I didn't make/discover any part of this glitch, I merely tested and compiled the work of others into this guide. Here are my sources:

* u/UW_Unknown_Warrior's [Reddit thread](https://nm.reddit.com/r/pokemon/comments/4a6abq/guide_getting_any_pok%C3%A9mon_you_want_in_gold_silver/) to the BOX9 ACE setup
* [Evie (ChickasaurusGL) on YouTube](https://www.youtube.com/user/ChickasaurusGL), primarily:
    * [Infinite Rare Candy](https://www.youtube.com/watch?v=CiDi5nb-uoc) (setup for setting balls slot 1 to rare candy)
    * [Get any item](https://www.youtube.com/watch?v=eUanqOkBlWA) (3-part setup to get ä, 255 of all TMs, and transforming items)
