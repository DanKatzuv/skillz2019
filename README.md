# SkillZ 2019
This is The PeaceMakers' code for the 2019 [SkillZ](https://pub.skillz-edu.org/portal/playground/) challenge, [_The Curse of Zadoom_](https://pub.skillz-edu.org/portal/games/6).

## Game Rules Summary
_The Curse of Zadoom_ is played by two players, one against the other. Each player has a Castle, two Elves and one pre-built Portal. Each player's objective is to destroy the enemy's Castle. Players can do so with Elves and Lava Giants, and Ice Trolls are used to defend from enemy creatures. While players can determine their Elves' location, Lava Giants go directly to the enemy Castle and Ice Trolls attack the nearest enemy creature. Players can use the Elves to build Portals which can summon Lava Giants and Ice Trolls. For more information about the game, please read [here](https://docs.google.com/presentation/d/1TE4X3sAsLtyexmazQLNSUCtX5StqMEKLaj0NNTgsGvc/edit#slide=id.g26a36cee9d_0_73).

## Our Strategy
- One Elf builds one more Portal near our Castle at the beginning of the match.
- Portals which are a [fixed distance](https://github.com/katzuv/skillz2019/blob/master/mainbot.py#L9) from the Castle are defined as _Defense Portals_, and they summon Ice Trolls only. All other Portals are defined as _Attack Portals_ and summon Lava Giants. If an Attack Portal [is endangered](https://github.com/katzuv/skillz2019/blob/master/mainbot.py#L129-L132), that is there's an Elf who can attack this Portal, it switches to summoning Ice Trolls to defend itself.
- When one of the Elves dies, the other retreats back to the Castle.
- Elves attack enemy Portals and Elves, but their first priority is rebuilding  Portals if they are destroyed.
