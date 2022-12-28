import 'package:balance_home_app/config/router.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter/foundation.dart';
// ignore: depend_on_referenced_packages
import 'package:adaptive_breakpoints/adaptive_breakpoints.dart';

/// Utils for platform detection
class PlatformUtils {
  // Whether is web environment
  bool get isWeb => kIsWeb;

  // Whether is mobile environment
  bool get isMobile =>
      (defaultTargetPlatform == TargetPlatform.android ||
          defaultTargetPlatform == TargetPlatform.iOS) &&
      !isWeb;

  // Whether is desktop or web environment
  bool get isDesktopOrWeb =>
      defaultTargetPlatform == TargetPlatform.windows ||
      defaultTargetPlatform == TargetPlatform.macOS ||
      defaultTargetPlatform == TargetPlatform.linux ||
      isWeb;

  /// Gets the platform where the application is executed.
  ///
  /// Web is not included.
  TargetPlatform get targetPlatform => defaultTargetPlatform;
  
  // Whether the platform window is considered as large
  bool isLargeWindow(BuildContext context) =>
    getWindowType(navigatorKey.currentContext!) >= AdaptiveWindowType.large;
  
  // Whether the platform window is considered as medium
  bool isMediumWindow(BuildContext context) =>
    getWindowType(navigatorKey.currentContext!) == AdaptiveWindowType.medium;
  
  // Whether the platform window is considered as small
  bool isSmallWindow() =>
    getWindowType(navigatorKey.currentContext!) == AdaptiveWindowType.small 
    || getWindowType(navigatorKey.currentContext!) == AdaptiveWindowType.xsmall;
}