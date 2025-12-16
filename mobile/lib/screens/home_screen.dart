import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _apiService = ApiService();
  Map<String, dynamic>? _userData;
  Map<String, dynamic>? _stats;
  List<dynamic> _attendance = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() => _isLoading = true);

    try {
      await _apiService.loadCredentials();
      final employeeId = _apiService.employeeId;
      
      if (employeeId != null) {
        final userData = await _apiService.getUserByEmployeeId(employeeId);
        final userId = userData['user']['id'];
        
        final stats = await _apiService.getUserStats(userId);
        final attendance = await _apiService.getUserAttendance(userId);

        setState(() {
          _userData = userData['user'];
          _stats = stats;
          _attendance = attendance;
          _isLoading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Xatolik: ${e.toString()}')),
        );
      }
      setState(() => _isLoading = false);
    }
  }

  Future<void> _logout() async {
    await _apiService.logout();
    if (mounted) {
      Navigator.pushReplacementNamed(context, '/login');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Davomat Tizimi'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadData,
          ),
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: _logout,
          ),
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _loadData,
              child: SingleChildScrollView(
                physics: const AlwaysScrollableScrollPhysics(),
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // Profile Card
                    Card(
                      elevation: 4,
                      child: Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: Row(
                          children: [
                            CircleAvatar(
                              radius: 40,
                              backgroundColor: Colors.blue.shade700,
                              child: Text(
                                _userData?['full_name']?.substring(0, 1).toUpperCase() ?? 'U',
                                style: const TextStyle(fontSize: 32, color: Colors.white),
                              ),
                            ),
                            const SizedBox(width: 16),
                            Expanded(
                              child: Column(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  Text(
                                    _userData?['full_name'] ?? 'Loading...',
                                    style: Theme.of(context).textTheme.titleLarge,
                                  ),
                                  const SizedBox(height: 4),
                                  Text(
                                    'ID: ${_userData?['employee_id'] ?? ''}',
                                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                                          color: Colors.grey.shade600,
                                        ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                    const SizedBox(height: 16),

                    // Stats Cards
                    Text(
                      'Statistika (30 kun)',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: _buildStatCard(
                            'Kelganlar',
                            _stats?['present']?.toString() ?? '0',
                            Colors.green,
                            Icons.check_circle,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: _buildStatCard(
                            'Kechikkanlar',
                            _stats?['late']?.toString() ?? '0',
                            Colors.orange,
                            Icons.access_time,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: _buildStatCard(
                            'Kelmaganlar',
                            _stats?['absent']?.toString() ?? '0',
                            Colors.red,
                            Icons.cancel,
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: _buildStatCard(
                            'Davomat %',
                            '${_stats?['attendance_rate']?.toStringAsFixed(0) ?? '0'}%',
                            Colors.blue,
                            Icons.trending_up,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 24),

                    // Attendance History
                    Text(
                      'Davomat Tarixi',
                      style: Theme.of(context).textTheme.titleLarge,
                    ),
                    const SizedBox(height: 12),
                    _attendance.isEmpty
                        ? const Card(
                            child: Padding(
                              padding: EdgeInsets.all(32.0),
                              child: Center(
                                child: Text('Davomat yozuvlari yo\'q'),
                              ),
                            ),
                          )
                        : ListView.builder(
                            shrinkWrap: true,
                            physics: const NeverScrollableScrollPhysics(),
                            itemCount: _attendance.length,
                            itemBuilder: (context, index) {
                              final record = _attendance[index];
                              final date = DateTime.parse(record['check_in_time']);
                              final isPresent = record['status'] == 'present';

                              return Card(
                                margin: const EdgeInsets.only(bottom: 8),
                                child: ListTile(
                                  leading: CircleAvatar(
                                    backgroundColor: isPresent ? Colors.green : Colors.orange,
                                    child: Icon(
                                      isPresent ? Icons.check : Icons.access_time,
                                      color: Colors.white,
                                    ),
                                  ),
                                  title: Text(DateFormat('dd MMM yyyy').format(date)),
                                  subtitle: Text(DateFormat('HH:mm').format(date)),
                                  trailing: Text(
                                    isPresent ? 'Keldi' : 'Kechikdi',
                                    style: TextStyle(
                                      color: isPresent ? Colors.green : Colors.orange,
                                      fontWeight: FontWeight.bold,
                                    ),
                                  ),
                                ),
                              );
                            },
                          ),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildStatCard(String title, String value, Color color, IconData icon) {
    return Card(
      elevation: 2,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Icon(icon, size: 32, color: color),
            const SizedBox(height: 8),
            Text(
              value,
              style: TextStyle(
                fontSize: 24,
                fontWeight: FontWeight.bold,
                color: color,
              ),
            ),
            const SizedBox(height: 4),
            Text(
              title,
              style: Theme.of(context).textTheme.bodySmall,
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
