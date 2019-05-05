# BrickPi NXT adventures

Over 10 years ago I bought a [Lego Mindstorms NXT][mindstorms_nxt] kit and
[played][haifux_lecture] with it a bit. Then life got in the way: I got
married, had kids, relocated countries, moved houses, you know, stuff. The kit
moved with me, forgotten and collecting dust. But then my older son got old
enough to show interest in both [Lego Technic][klutz_book] and
[Python][vorderman], and I figured it's time to dig up the NXT kit from the
attic and see if it works.

Unfortunately, the [LCD ribbon was bust][lcd_ribbon_rip] and I couldn't fix it,
but everything else seemed to be working, so I got the really nice [Dexter
Industries BrickPi][dexter] kit, you know, for the kid. He really liked it, and
could follow along a fairly imperative flow ("hear sound, activate mottor until
button pressed"), but there's a limit to what you can do that way. So the next
week his dad pulled a late night "to refactor a little bit". And... well, here
we are. I guess I am the real kid here.

[mindstorms_nxt]: https://en.wikipedia.org/wiki/Lego_Mindstorms_NXT
[haifux_lecture]: http://haifux.org/hebrew/lectures/207/nxt-screen.pdf
[klutz_book]: https://www.amazon.co.uk/Lego-Crazy-Action-Contraptions-Klutz/dp/1591747694/
[vorderman]: https://www.amazon.co.uk/Computer-Coding-Python-Projects-Step/dp/0241286867/
[lcd_ribbon_rip]: https://www.google.com/search?q=lego+nxt+lcd+ribbon
[dexter]: https://www.dexterindustries.com/brickpi/

## Projects

### Sound seeking robot

Status: *in progress*

The idea here is to create an autonomous robot that can find a sound source in
a room. So, for example, if you put the robot in a room with a phone playing a
fixed 1.7Khz tone, the robot should move closer to the phone. I've equipped it
with two sound sensors, a compass, and a distance sensor (not yet in use). The
idea is to use the volume difference between the two sound sensors to figure
out the right angle on the compass to steer towards.

![Picture of this robot](http://i67.tinypic.com/11jmzgk.jpg "I wish I had source control for Lego blocks...")

A few more photos here [here][photos]. The resulting data samples look [like
this][samples]. I'll keep y'all posted how it pans out.

[photos]: https://imgur.com/a/FtwpkFA
[samples]: https://docs.google.com/spreadsheets/d/1GRGO3dPiG_4B-m1wMhrmS3kf7z2w3d36XyGFu_e0TsA/edit#gid=525440628
