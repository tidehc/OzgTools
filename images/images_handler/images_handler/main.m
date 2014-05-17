//
//  main.m
//  images_handler
//
//  Created by 欧 志刚 on 13-10-2.
//  Copyright (c) 2013年 欧 志刚. All rights reserved.
//

#import <Foundation/Foundation.h> //引用Foundation.framework
#import <AppKit/AppKit.h> //引用AppKit.framework
#import <CoreGraphics/CoreGraphics.h> //引用CoreGraphics.framework

//参数1：需要放缩的文件夹
//参数2：目标文件夹
//参数3：目标宽度
//参数4：目标高度
//参数5：主宽度
//参数6：主高度

//处理一个图片，srcPath(原图路径)，targetDir(目标文件夹)，scaleWidth(目标宽度), scaleHeight(目标高度), mainWidth(主宽度), mainHeight(主高度)
void handlerImage(NSString* srcPath, NSString* targetDir, CGFloat scaleWidth, CGFloat scaleHeight, CGFloat mainWidth, CGFloat mainHeight)
{
    NSFileManager *fileManager = [NSFileManager defaultManager];
    
    //目标文件夹不存在则建立文件夹
    if(![fileManager fileExistsAtPath:targetDir])
        [fileManager createDirectoryAtPath:targetDir withIntermediateDirectories:YES attributes:nil error:nil];
    
    //获取src的文件名
    NSArray *srcPathComponents = srcPath.pathComponents;
    NSString *targetPath = [NSString stringWithFormat:@"%@/%@", targetDir, [srcPathComponents objectAtIndex:srcPathComponents.count - 1]];
    
    //原图
    NSImage *srcImg = [[NSImage alloc] initWithData:[NSData dataWithContentsOfFile:srcPath]];
    NSImageRep *srcRep = [[srcImg representations] objectAtIndex:0];
    NSSize srcImageSize = NSMakeSize(srcRep.pixelsWide, srcRep.pixelsHigh);
    
    //计算宽高
    scaleWidth = srcImageSize.width / mainWidth * scaleWidth;
    scaleHeight = srcImageSize.height / mainHeight * scaleHeight;
    
    //新的大小
    NSSize newSize = NSMakeSize(scaleWidth, scaleHeight);
    
    //目标图片
    NSImage *targetImg = [[NSImage alloc] initWithSize:newSize];
    
    //放缩目标图片
    [targetImg lockFocus];
    [srcImg setSize: newSize];
    [[NSGraphicsContext currentContext] setImageInterpolation:NSImageInterpolationHigh];
    [srcImg drawAtPoint:NSZeroPoint fromRect:CGRectMake(0, 0, newSize.width, newSize.height) operation:NSCompositeCopy fraction:1.0];
    
    NSBitmapImageRep *bits = [[[NSBitmapImageRep alloc]initWithFocusedViewRect:NSMakeRect(0, 0, newSize.width, newSize.height)] autorelease];
    
    [targetImg unlockFocus];
    
    //保存图
    NSDictionary *targetImgProps = [NSDictionary dictionaryWithObject:[NSNumber numberWithBool:0] forKey:NSImageCompressionFactor];
    NSData *targetImgData = [bits representationUsingType:NSPNGFileType properties:targetImgProps];
    [targetImgData writeToFile:targetPath atomically:YES];
    
    [targetImg release];
    [srcImg release];
    
    NSLog(@"原图的路径：%@ 处理后的路径：%@", srcPath, targetPath);
}

//开始执行，srcDir(原图目录)，targetDir(目标文件夹)，scaleWidth(目标宽度), scaleHeight(目标高度), mainWidth(主宽度), mainHeight(主高度)
void startHandlerDir(NSString* srcDir, NSString* targetDir, CGFloat scaleWidth, CGFloat scaleHeight, CGFloat mainWidth, CGFloat mainHeight)
{
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSArray *fileNameList = [fileManager contentsOfDirectoryAtPath:srcDir error:nil];
    for (NSString *fileName in fileNameList)
    {
        NSString* fileAllName = [NSString stringWithFormat:@"%@/%@", srcDir, fileName];
        
        if(![fileName.pathExtension isEqualToString:@""] && [fileName.pathExtension isEqualToString:@"png"])
        {
            //如果不是文件夹，而且是png文件，则执行图片处理
            
            handlerImage(fileAllName, targetDir, scaleWidth, scaleHeight, mainWidth, mainHeight);
            
        }
        else if([fileName.pathExtension isEqualToString:@""])
        {
            //如果是文件夹则使用递归
            startHandlerDir(fileAllName, [NSString stringWithFormat:@"%@/%@", targetDir, fileName], scaleWidth, scaleHeight, mainWidth, mainHeight);
            
            //NSLog(@"%@", fileAllName);
            //NSLog(@"%@", [NSString stringWithFormat:@"%@/%@", targetDir, fileName]);
        }
    }
    
}

int main(int argc, const char * argv[])
{

    @autoreleasepool
    {
        
        startHandlerDir([NSString stringWithUTF8String:argv[1]], [NSString stringWithUTF8String:argv[2]], [[NSString stringWithUTF8String:argv[3]] floatValue], [[NSString stringWithUTF8String:argv[4]] floatValue], [[NSString stringWithUTF8String:argv[5]] floatValue], [[NSString stringWithUTF8String:argv[6]] floatValue]);
        
        NSLog(@"完成");
    }
    return 0;
}
