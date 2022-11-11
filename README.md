# Dungeon and Platformer Blending using CVAEs

Code for Procedural Content Generation using Behavior Trees (PCGBT), EXAG 2021

Paper: https://arxiv.org/abs/2107.06638

Citation:
```
@inproceedings{sarkar2021pcgbt,
  title={Procedural Content Generation using Behavior Trees (PCGBT)},
  author={Sarkar, Anurag and Cooper, Seth},
  booktitle = {Proceedings of the Experimental AI in Games (EXAG) Workshop at AIIDE},
  year={2021}
}
```

Base behavior tree implementation taken from:
https://github.com/splintered-reality/py_trees


Usage:
* Game options:
    * smb
    * mm
    * met
    * zelda
    * blend
    * generic

* Additional args control level properties relevant to each game:
    * smb - pp (paths & pipes), gv (gaps and valleys)
    * mm - hp (horizontal segments), vp (vertical segments), loop (use looping BT), num (number of segments when using looping BT)
    * zelda/met - num (number of rooms/segments in level)
    * generic - gen (game (met or mm) with which to instantiate generic BT), hsize (size of horizontal section), loop (use looping BT), num (number of segments when using looping BT)
    * blend - mmsize (size of Mega Man horizontal section), metsize (size of Metroid horizontal section)

* Examples
    * `python main.py --game smb --pp 0.7 --gv 0.2 --name test_level`
    * `python main.py --game mm --hp 0.8 --vp 0.1`
    * `python main.py --game mm --num 15 --loop`
    * `python main.py --game zelda --num 12`
    * `python main.py --game met --num 7`
    * `python main.py --game generic --gen met --hsize 5` 
    * `python main.py --game generic --gen mm --num 12 --loop`
    * `python main.py --game blend --mmsize 2 --metsize 6`
