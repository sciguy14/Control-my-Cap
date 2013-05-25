/*
 * flatOpenBracelet.scad
 * 
 * Written by aubenc @ Thingiverse
 *
 * http://www.thingiverse.com/thing:17083
 *
 *	Licensed under the Creative Commons Public Domain license
 *
 * Usage:
 *
 *		Features:
 *
 *		1. A central section for the texture of your bracelet.
 *
 *		2. Texture section surronded by two flat sections.
 *
 *		3.	Almost rounded edges. Rounded with a little flat to make it easy
 *			to stick to the build platform, the size of the flat is determined
 *			by your desired overhang angle.
 *
 *		4. Asimetrical construction (thinner at the opening side) for a
 *			texture fadding effect.
 *
 *		Set the parameters to the desired values...
 *
 *			For a circular  Bracelet set both "yas" and "xas" to
 *			the same value.
 *
 *			Add a module with the design of your texture and use the
 *			boolean intersection() for your module and envelope() module.
 */


/* *************** Parameters *********************************************** */

yas=60;		// Y axis inner diameter of the ring/bracelet
xas=50;		// X axis inner diameter of the ring/bracelet
thg=1.5;		// Texture Cut Depth
twd=20;		// Texture Width
dfw=1.5;		// Flat non textured width at each end
mwt=2.1;		// Minimum Wall Thickness
rlf=60;		// Angle to start the roundness for the edges
osz=20;		// Opening size


				// Don't set the following parameter to zero!
				// (unless you enjoy running into division by zero errors)
				//
res=1;		// Ressolution, +/- face each [value]mm of perimeter 
				// 	High value for a quicker rendering.
				//		Low value for a smooth finishing.


/* *************** Computed / Hardcoded ************************************* */

rid=yas;						// Ring inner diameter
rod=rid+2*(mwt+thg);		// Ring outer diameter
rwd=twd+2*dfw;				// Ring width
tcr=(pow(thg,2)+pow(twd/2,2))/2/thg;	// Texture carve circle radius
tco=rod/2+tcr-thg;		//	Texture carve circle traslation
rhg=(mwt+thg)*sin(rlf);	// Rounded edge ring height
tth=twd+2*(thg+rhg);		// Total height
fct=4*round(rod*PI/res/4);		// Facets for the bracelet circle

echo("Total Height: ",tth);


/* *************** Modulers ************************************************* */

	envelope();


/* *************** Code ***************************************************** */

module envelope()
{
	scale([xas/yas,1,1])
	intersection()
	{
		bracelet_ring();
		raw_shape();
		texture_fadding();
	}
}

module bracelet_ring()
{
	difference()
	{
		rounded_block();

		translate([0,0,-0.1])
		cylinder(h=tth+0.2, r=rid/2, $fn=fct, center=false);
	}
}

module raw_shape()
{
	olf=asin(osz/(2*sqrt(pow(osz/2,2)+pow(rod/2,2))));

	x0=0;						x1=rod/2+0.1;
	y0=tth/2/cos(olf);	y1=y0+rod/2*tan(olf);

	translate([0,0,tth/2])
	if( osz == 0 )
	{
		cube(size=[rod,rod,tth], center=true);
	}
	else
	{
		union()
		{
			difference()
			{
				cube(size=[rod,rod,tth], center=true);

				linear_extrude(height=tth+0.2, center=true, convexity=10)
				polygon(points=[ [x0,y0],[x1,y1],[x1,-y1],[x0,-y0] ],
							paths=[ [0,1,2,3] ]);
			}

			for(i=[-1,1])
			{
				rotate([0,90,i*olf])
				translate([0,i*tth/2,0])
				cylinder(h=rod, r=tth/2, $fn=4*round(tth*PI/res/4), center=false);
			}
		}
	}
}

module texture_fadding()
{
	translate([-thg,0,0])
	union()
	{
		rounded_block();

		cylinder(h=tth, r=(rod+rid)/4, $fn=fct, center=false);
	}
}

module rounded_block()
{
	union()
	{
		translate([0,0,rhg/2]) rounded_edge();

		translate([0,0,rhg/2])
		cylinder(h=tth-rhg, r=rod/2, $fn=fct, center=false);

		translate([0,0,tth-rhg/2]) rounded_edge();
	}
}

module rounded_edge()
{
	intersection()
	{
		cube(size=[rod+1,rod+1,rhg], center=true);

		rotate_extrude($fn=fct, convexity=10)
		translate([(rid+mwt+thg)/2,0,0])
		circle(r=(mwt+thg)/2, $fn=(rod-rid)*PI/res);
	}
}