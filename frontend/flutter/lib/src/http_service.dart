import 'dart:convert';
import 'dart:developer';
// ignore: depend_on_referenced_packages
import 'package:flutter/foundation.dart';
import 'package:balance_home_app/config/environment.dart';
import 'package:balance_home_app/config/api_contract.dart';
import 'package:balance_home_app/src/core/presentation/views/error_view.dart';
import 'package:balance_home_app/src/features/auth/domain/entities/credentials_entity.dart';
import 'package:balance_home_app/src/features/auth/domain/entities/jwt_entity.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
// ignore: depend_on_referenced_packages, implementation_imports
import 'package:http_parser/src/media_type.dart' as mt;
import 'package:universal_io/io.dart' as io;

/// Encapsulates the proccess of making authorized HTTP requests from the services.
///
/// This allows for mocking all HTTP requests in service testing and also,
/// reduces code duplication by abstracting this proccess.
class HttpService {
  /// Client that will make all requests
  final http.Client _client;

  JwtEntity? _jwtEntity;

  final FlutterSecureStorage _secureStorage;

  /// Creates an [HttpService].
  ///
  /// The optional [http.CLient] argument is added for testing purposes.
  HttpService({http.Client? client, FlutterSecureStorage? secureStorage})
      : _client = client ?? http.Client(),
        _secureStorage = secureStorage ?? const FlutterSecureStorage();

  /// Gets the base url of the server using environment variables.
  String baseUrl = Environment.apiUrl;

  /// Returns the necessary content and authentication headers for all server requests.
  Map<String, String> getHeaders() {
    Map<String, String> headers = {
      "Content-Type": io.ContentType.json.toString(),
      "Accept-Language": "en"
    };
    if (_jwtEntity != null) {
      headers["Authorization"] = "Bearer ${_jwtEntity!.access}";
    }
    return headers;
  }

  /// Sends a [GET] request to [baseUrl]/[subPath].
  Future<HttpResponse> sendGetRequest(String subPath) async {
    try {
      HttpResponse response = _createHttpResponse(await _client
          .get(Uri.parse("$baseUrl$subPath"), headers: getHeaders()));
      if (await _shouldRepeatResponse(response)) {
        // Recursive call
        return await sendGetRequest(subPath);
      }
      return response;
    } catch (e) {
      log("${Uri.parse("$baseUrl$subPath")} -> $e");
      return HttpResponse(500, {"message": e.toString()});
    }
  }

  /// Sends a `POST` request to `baseUrl`/`subPath` with `body` as the content.
  Future<HttpResponse> sendPostRequest(
      String subPath, Map<String, dynamic> body) async {
    try {
      HttpResponse response = _createHttpResponse(await _client.post(
          Uri.parse("$baseUrl$subPath"),
          headers: getHeaders(),
          body: jsonEncode(body)));
      if (await _shouldRepeatResponse(response)) {
        // Recursive call
        return await sendPostRequest(subPath, body);
      }
      return response;
    } catch (e) {
      log("${Uri.parse("$baseUrl$subPath")} -> $e");
      return HttpResponse(500, {"message": e.toString()});
    }
  }

  /// Sends a `PATCH` multipart request to upload the image located at `filePath` to `baseUrl`/`subPath`.
  Future<HttpResponse> sendPatchImageRequest(
      String subPath, Uint8List imageBytes, String imageType) async {
    try {
      http.MultipartFile httpImage = http.MultipartFile.fromBytes(
          'image', imageBytes,
          contentType: mt.MediaType.parse(imageType),
          filename: 'upload_image.${imageType.split("/").last}');
      final request =
          http.MultipartRequest('PATCH', Uri.parse("$baseUrl$subPath"));
      request.files.add(httpImage);
      if (_jwtEntity != null) {
        request.headers["Authorization"] = "Bearer ${_jwtEntity!.access}";
      }
      http.StreamedResponse res = (await _client.send(request));
      Map<String, dynamic> content = {};
      try {
        content = json.decode(utf8.decode(await res.stream.toBytes()));
      }
      catch (_) {}
      HttpResponse response =
          HttpResponse(res.statusCode, content);
      if (await _shouldRepeatResponse(response)) {
        // Recursive call
        return await sendPatchImageRequest(subPath, imageBytes, imageType);
      }
      return response;
    } catch (e) {
      log("${Uri.parse("$baseUrl$subPath")} -> $e");
      return HttpResponse(500, {"message": e.toString()});
    }
  }

  /// Sends a `PUT` request to `baseUrl`/`subPath` and with `body` as content.
  Future<HttpResponse> sendPutRequest(
      String subPath, Map<String, dynamic> body) async {
    try {
      HttpResponse response = _createHttpResponse(await _client.put(
          Uri.parse("$baseUrl$subPath"),
          headers: getHeaders(),
          body: jsonEncode(body)));
      if (await _shouldRepeatResponse(response)) {
        // Recursive call
        return await sendPutRequest(subPath, body);
      }
      return response;
    } catch (e) {
      log("${Uri.parse("$baseUrl$subPath")} -> $e");
      return HttpResponse(500, {"message": e.toString()});
    }
  }

  /// Sends a `PATCH` request to `baseUrl`/`subPath` and with `body` as content.
  Future<HttpResponse> sendPatchRequest(
      String subPath, Map<String, dynamic> body) async {
    try {
      HttpResponse response = _createHttpResponse(await _client.patch(
          Uri.parse("$baseUrl$subPath"),
          headers: getHeaders(),
          body: jsonEncode(body)));
      if (await _shouldRepeatResponse(response)) {
        // Recursive call
        return await sendPatchRequest(subPath, body);
      }
      return response;
    } catch (e) {
      log("${Uri.parse("$baseUrl$subPath")} -> $e");
      return HttpResponse(500, {"message": e.toString()});
    }
  }

  /// Sends a `DEL` request to `baseUrl`/`subPath`.
  Future<HttpResponse> sendDelRequest(String subPath) async {
    try {
      HttpResponse response = _createHttpResponse(await _client
          .delete(Uri.parse("$baseUrl$subPath"), headers: getHeaders()));
      if (await _shouldRepeatResponse(response)) {
        // Recursive call
        return await sendDelRequest(subPath);
      }
      return response;
    } catch (e) {
      log("${Uri.parse("$baseUrl$subPath")} -> $e");
      return HttpResponse(500, {"message": e.toString()});
    }
  }

  HttpResponse _createHttpResponse(http.Response response) {
    Map<String, dynamic> jsonResponse =
        json.decode(const Utf8Decoder().convert(response.bodyBytes))
            as Map<String, dynamic>;
    HttpResponse httpResponse = HttpResponse(response.statusCode, jsonResponse);
    return httpResponse;
  }

  Future<bool> _shouldRepeatResponse(HttpResponse response) async {
    if (response.statusCode == 401) {
      HttpResponse newResponse = response;
      if (_jwtEntity != null) {
        // Try to refresh token in case 401 response
        newResponse = _createHttpResponse(await _client.post(
            Uri.parse("$baseUrl${APIContract.jwtRefresh}"),
            headers: getHeaders(),
            body: jsonEncode({"refresh": _jwtEntity!.refresh})));
      } else {
        String? refreshJwt = await _secureStorage.read(key: "refresh_jwt");
        if (refreshJwt != null) {
          newResponse = _createHttpResponse(await _client.post(
              Uri.parse("$baseUrl${APIContract.jwtRefresh}"),
              headers: getHeaders(),
              body: jsonEncode({"refresh": refreshJwt})));
          if (newResponse.statusCode != 401 && newResponse.statusCode != 400) {
            setJwtEntity(JwtEntity(
                access: newResponse.content["access"], refresh: refreshJwt));
            return true;
          }
        }
      }
      // If 401 is recived it should be tried with stored credentials
      if (newResponse.statusCode == 401 && newResponse.statusCode != 400) {
        setJwtEntity(null); // Current token is not valid
        String? email = await _secureStorage.read(key: "email");
        String? password = await _secureStorage.read(key: "password");
        if (email != null && password != null) {
          newResponse = _createHttpResponse(await _client.post(
              Uri.parse("$baseUrl${APIContract.jwtLogin}"),
              headers: getHeaders(),
              body: jsonEncode(
                  CredentialsEntity(email: email, password: password)
                      .toJson())));
          if (newResponse.statusCode != 401 && newResponse.statusCode != 400) {
            // Update current JWT
            setJwtEntity(JwtEntity.fromJson(newResponse.content));
            return true;
          }
        }
      } else if (_jwtEntity != null) {
        // Update current JWT
        setJwtEntity(JwtEntity(
            access: newResponse.content["access"],
            refresh: _jwtEntity!.refresh));
        return true;
      }
    }
    if (response.statusCode == 500) ErrorView.go();
    return false;
  }

  void setJwtEntity(JwtEntity? jwt) {
    _jwtEntity = jwt;
  }
}

class HttpResponse {
  final int statusCode;

  final Map<String, dynamic> content;

  /// Whether [statusCode] is not a 20X code
  bool get hasError => (statusCode / 10).round() != 20;

  /// Get first message error in the content json if content is not empty
  String get errorMessage => (content.keys.isEmpty)
      ? ""
      : (content[content.keys.first] is! List)
          ? "${content.keys.first} : ${content[content.keys.first]}"
          : "${content.keys.first} : ${(content[content.keys.first] as List).first}";

  HttpResponse(this.statusCode, this.content);
}
