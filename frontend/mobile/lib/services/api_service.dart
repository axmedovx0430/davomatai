import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class ApiService {
  static const String baseUrl = 'http://your-backend-url.com'; // Update this
  
  String? _apiKey;
  String? _employeeId;

  Future<void> saveCredentials(String employeeId, String apiKey) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('employee_id', employeeId);
    await prefs.setString('api_key', apiKey);
    _employeeId = employeeId;
    _apiKey = apiKey;
  }

  Future<bool> loadCredentials() async {
    final prefs = await SharedPreferences.getInstance();
    _employeeId = prefs.getString('employee_id');
    _apiKey = prefs.getString('api_key');
    return _employeeId != null && _apiKey != null;
  }

  Future<void> logout() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.clear();
    _employeeId = null;
    _apiKey = null;
  }

  Map<String, String> _getHeaders() {
    return {
      'Content-Type': 'application/json',
      if (_apiKey != null) 'X-API-Key': _apiKey!,
    };
  }

  Future<Map<String, dynamic>> getUserByEmployeeId(String employeeId) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/users/employee/$employeeId'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load user');
    }
  }

  Future<List<dynamic>> getTodayAttendance() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/attendance/today'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['attendance'] ?? [];
    } else {
      throw Exception('Failed to load attendance');
    }
  }

  Future<List<dynamic>> getUserAttendance(int userId, {int days = 30}) async {
    final endDate = DateTime.now();
    final startDate = endDate.subtract(Duration(days: days));
    
    final response = await http.get(
      Uri.parse(
        '$baseUrl/api/attendance/user/$userId?start_date=${startDate.toIso8601String().split('T')[0]}&end_date=${endDate.toIso8601String().split('T')[0]}'
      ),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['attendance'] ?? [];
    } else {
      throw Exception('Failed to load user attendance');
    }
  }

  Future<Map<String, dynamic>> getUserStats(int userId, {int days = 30}) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/attendance/user/$userId/stats?days=$days'),
      headers: _getHeaders(),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['stats'] ?? {};
    } else {
      throw Exception('Failed to load stats');
    }
  }

  String? get employeeId => _employeeId;
}
