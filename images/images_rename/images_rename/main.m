//
//  main.m
//  images_rename
//
//  Created by ozg on 13-10-4.
//  Copyright (c) 2013年 ozg. All rights reserved.
//

#import <Foundation/Foundation.h>

//参数1：需要改名的文件夹
//参数2：文件名的后缀

//文件改名
void fileReanme(NSString* srcPath, NSString* newPath)
{
    NSFileManager *fileManager = [NSFileManager defaultManager];
    
    [fileManager moveItemAtPath:srcPath toPath:newPath error:nil];
}

//srcDir（文件夹），suffix（文件名后缀）
void startHandlerDir(NSString* srcDir, NSString* suffix)
{
    NSFileManager *fileManager = [NSFileManager defaultManager];
    NSArray *fileNameList = [fileManager contentsOfDirectoryAtPath:srcDir error:nil];
    for (NSString *fileName in fileNameList)
    {
        NSString* fileAllName = [NSString stringWithFormat:@"%@/%@", srcDir, fileName];
        
        if(![fileName.pathExtension isEqualToString:@""] && [fileName.pathExtension isEqualToString:@"png"])
        {
            //如果不是文件夹，而且是png文件，则执行处理
            
            NSArray *fileNameSplit = [fileName componentsSeparatedByString:@"."];
            fileReanme(fileAllName, [NSString stringWithFormat:@"%@/%@%@.%@", srcDir, [fileNameSplit objectAtIndex:0], suffix, [fileNameSplit objectAtIndex:1]]);
        }
        else if([fileName.pathExtension isEqualToString:@""])
        {
            //如果是文件夹则使用递归
            startHandlerDir(fileAllName, suffix);
            
            //NSLog(@"%@", fileAllName);
            //NSLog(@"%@", [NSString stringWithFormat:@"%@/%@", targetDir, fileName]);
        }
    }
    
}

int main(int argc, const char * argv[])
{

    @autoreleasepool {
        
        startHandlerDir([NSString stringWithUTF8String:argv[1]], [NSString stringWithUTF8String:argv[2]]);
        
        NSLog(@"完成");
        
    }
    return 0;
}

