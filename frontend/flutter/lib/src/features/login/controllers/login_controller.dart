import 'package:flutter_riverpod/flutter_riverpod.dart';

/*
final loginControllerProvider = StateNotifierProvider<LoginNotifier, LoginState>(
  (ref) {
    return LoginNotifier(ref);
  }
);


class LoginNotifier extends StateNotifier<LoginState> {
  final Ref ref;
  
  LoginNotifier(this.ref) : super(const LoginStateInitial());

  void login(String email, String password) async {
    state = const LoginStateLoading();
    try {
      await ref.read(authProvider).login(
        email, password);
      state = const LoginStateSuccess();
    } catch (e) {
      state = LoginStateError(e.toString());
    }
  }
}
*/