//
//  IntroScene.m
//  plist_to_images
//
//  Created by ozg on 14-5-16.
//  Copyright ozg 2014年. All rights reserved.
//
// -----------------------------------------------------------------------

#import "IntroScene.h"

#define PLIST_PATH @"plist_image/Fishall.plist"
#define SAVE_DIR @"/Users/ozg/Desktop/_hanlde_images2/"

UIImage* convertSpriteToImage(CCSprite* sprite)
{
    CGPoint p = sprite.anchorPoint;
    [sprite setAnchorPoint:ccp(0, 0)];
    CCRenderTexture *renderer = [CCRenderTexture renderTextureWithWidth:sprite.contentSize.width height:sprite.contentSize.height];
    [renderer begin];
    [sprite visit];
    [renderer end];
    [sprite setAnchorPoint:p];
    return [renderer getUIImage];
}

@implementation IntroScene

+ (IntroScene *)scene
{
	return [[self alloc] init];
}

- (id)init
{
    // Apple recommend assigning self with supers return value
    self = [super init];
    if (!self) return(nil);
    
    [[CCSpriteFrameCache sharedSpriteFrameCache] addSpriteFramesWithFile:PLIST_PATH];
    
    NSDictionary *plist = [NSDictionary dictionaryWithContentsOfFile:[[NSBundle mainBundle] pathForResource:PLIST_PATH ofType:nil]];
    NSDictionary *frames = [plist objectForKey:@"frames"];
    for (NSString* imgName in frames.allKeys)
    {
        CCSprite *sprite = [CCSprite spriteWithSpriteFrame:[[CCSpriteFrameCache sharedSpriteFrameCache] spriteFrameByName:imgName]];
        
        NSString *savePath = [NSString stringWithFormat:@"%@/%@", SAVE_DIR, imgName];
        UIImage *img = convertSpriteToImage(sprite);
        [UIImagePNGRepresentation(img) writeToFile:savePath atomically:YES];
        
        NSLog(@"已保存到%@", savePath);
    }

	return self;
}

@end
