import Cocoa

// Original vector mark: an open book with ascending pages and a warm bookmark.
// Rasterized at every required icon size by the packaging script; no remote assets.
let size = NSSize(width:1024,height:1024)
let image = NSImage(size:size)
image.lockFocus()
let base = NSBezierPath(roundedRect:NSRect(x:72,y:72,width:880,height:880),xRadius:198,yRadius:198)
NSGradient(starting:NSColor(calibratedRed:0.36,green:0.34,blue:0.49,alpha:1),ending:NSColor(calibratedRed:0.20,green:0.19,blue:0.29,alpha:1))!.draw(in:base,angle:275)
NSColor(white:1,alpha:0.10).setStroke()
base.lineWidth=2;base.stroke()
func page(_ points:[NSPoint], _ color:NSColor) {
    let shape=NSBezierPath();shape.move(to:points[0])
    for p in points.dropFirst(){shape.line(to:p)}
    shape.close();color.setFill();shape.fill()
}
let cream=NSColor(calibratedRed:0.98,green:0.96,blue:0.91,alpha:1)
let lavender=NSColor(calibratedRed:0.72,green:0.70,blue:0.82,alpha:1)
// The pages share a spine. Their upper edges rise from left to right.
page([NSPoint(x:246,y:348),NSPoint(x:477,y:270),NSPoint(x:477,y:652),NSPoint(x:246,y:731)],lavender)
page([NSPoint(x:500,y:270),NSPoint(x:778,y:368),NSPoint(x:778,y:748),NSPoint(x:500,y:650)],cream)
page([NSPoint(x:500,y:295),NSPoint(x:727,y:393),NSPoint(x:727,y:783),NSPoint(x:500,y:683)],NSColor(calibratedRed:0.87,green:0.85,blue:0.92,alpha:1))
page([NSPoint(x:500,y:320),NSPoint(x:670,y:410),NSPoint(x:670,y:812),NSPoint(x:500,y:722)],cream)
page([NSPoint(x:584,y:766),NSPoint(x:623,y:786),NSPoint(x:623,y:644),NSPoint(x:603,y:661),NSPoint(x:584,y:642)],NSColor(calibratedRed:0.91,green:0.64,blue:0.43,alpha:1))
let line=NSBezierPath();line.move(to:NSPoint(x:289,y:595));line.line(to:NSPoint(x:430,y:547));line.move(to:NSPoint(x:289,y:540));line.line(to:NSPoint(x:397,y:503));line.lineWidth=9;line.lineCapStyle = .round;NSColor(calibratedRed:0.91,green:0.89,blue:0.96,alpha:0.7).setStroke();line.stroke()
image.unlockFocus()
let bitmap=NSBitmapImageRep(data:image.tiffRepresentation!)!
try bitmap.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:CommandLine.arguments[1]))
