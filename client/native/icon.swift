import Cocoa
let size=NSSize(width:1024,height:1024)
let image=NSImage(size:size)
image.lockFocus()
NSColor(calibratedRed:0.14,green:0.29,blue:0.25,alpha:1).setFill()
NSBezierPath(roundedRect:NSRect(x:40,y:40,width:944,height:944),xRadius:210,yRadius:210).fill()
let attrs:[NSAttributedString.Key:Any]=[.font:NSFont(name:"Georgia-Bold",size:660) ?? NSFont.boldSystemFont(ofSize:660),.foregroundColor:NSColor(calibratedRed:0.85,green:0.89,blue:0.62,alpha:1)]
let word="S" as NSString;let measured=word.size(withAttributes:attrs)
word.draw(at:NSPoint(x:(1024-measured.width)/2,y:(1024-measured.height)/2+10),withAttributes:attrs)
image.unlockFocus()
let bitmap=NSBitmapImageRep(data:image.tiffRepresentation!)!
try bitmap.representation(using:.png,properties:[:])!.write(to:URL(fileURLWithPath:CommandLine.arguments[1]))
