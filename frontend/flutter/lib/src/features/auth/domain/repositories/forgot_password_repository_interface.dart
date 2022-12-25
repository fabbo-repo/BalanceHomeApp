import 'package:balance_home_app/src/core/domain/failures/failure.dart';
import 'package:balance_home_app/src/features/auth/domain/entities/forgot_password_entity.dart';
import 'package:fpdart/fpdart.dart';

/// Forgot Password Repository Interface.
abstract class ForgotPasswordRepositoryInterface {
  /// Request forgot password code by `email`.
  Future<Either<Failure, void>> requestCode(String email);

  /// Request forgot password code verification.
  Future<Either<Failure, bool>> verifyCode(ForgotPasswordEntity entity);
}
