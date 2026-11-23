import 'package:material_ui/material_ui.dart';
import 'package:myportofolio_mobile/widgets/left_drawer.dart';

/// Halaman form untuk menambahkan riwayat pendidikan.
///
/// Field mengikuti model `Education` pada aplikasi Django:
/// `institution_name`, `level`, `field_of_study`, `gpa`, `start_year`,
/// `end_year`, dan `description`.
class EducationFormPage extends StatefulWidget {
  const EducationFormPage({super.key});

  @override
  State<EducationFormPage> createState() => _EducationFormPageState();
}

class _EducationFormPageState extends State<EducationFormPage> {
  final _formKey = GlobalKey<FormState>();

  /// Batas panjang `CharField(max_length=255)` pada model Django.
  static const int _maxCharLength = 255;

  /// Pilihan jenjang, sama dengan `Education.LEVEL_CHOICES`.
  static const Map<String, String> _levels = {
    'elementary': 'Elementary School',
    'junior_high': 'Junior High School',
    'senior_high': 'Senior High School',
    'diploma': 'Diploma',
    'bachelor': "Bachelor's Degree",
    'master': "Master's Degree",
    'doctorate': 'Doctorate',
  };

  final _institutionController = TextEditingController();
  final _fieldOfStudyController = TextEditingController();
  final _gpaController = TextEditingController();
  final _startYearController = TextEditingController();
  final _endYearController = TextEditingController();
  final _descriptionController = TextEditingController();

  String _level = 'bachelor'; // default sesuai model
  int? _startYear;
  int? _endYear; // null berarti masih berlangsung (ongoing)

  /// Format IPK: satu digit bilangan bulat dan maksimal dua desimal,
  /// mengikuti `DecimalField(max_digits=4, decimal_places=2)`.
  static final RegExp _gpaPattern = RegExp(r'^\d(\.\d{1,2})?$');

  @override
  void dispose() {
    _institutionController.dispose();
    _fieldOfStudyController.dispose();
    _gpaController.dispose();
    _startYearController.dispose();
    _endYearController.dispose();
    _descriptionController.dispose();
    super.dispose();
  }

  /// Membuka [showDatePicker] dalam mode tahun dan mengembalikan tahun
  /// yang dipilih, atau `null` jika dialog dibatalkan.
  Future<int?> _pickYear(int? initialYear) async {
    final now = DateTime.now();
    final picked = await showDatePicker(
      context: context,
      initialDate: DateTime(initialYear ?? now.year),
      firstDate: DateTime(1950),
      lastDate: DateTime(now.year + 10),
      initialDatePickerMode: DatePickerMode.year,
      helpText: 'Select year',
    );
    return picked?.year;
  }

  Future<void> _selectStartYear() async {
    final year = await _pickYear(_startYear);
    if (year == null) return;
    setState(() {
      _startYear = year;
      _startYearController.text = '$year';
    });
  }

  Future<void> _selectEndYear() async {
    final year = await _pickYear(_endYear ?? _startYear);
    if (year == null) return;
    setState(() {
      _endYear = year;
      _endYearController.text = '$year';
    });
  }

  void _clearEndYear() {
    setState(() {
      _endYear = null;
      _endYearController.clear();
    });
  }

  InputDecoration _decoration(String label, {String? hint}) {
    return InputDecoration(
      labelText: label,
      hintText: hint,
      border: OutlineInputBorder(borderRadius: BorderRadius.circular(5.0)),
    );
  }

  String? _validateInstitution(String? value) {
    final text = value?.trim() ?? '';
    if (text.isEmpty) {
      return 'Enter an institution name.';
    }
    if (text.length > _maxCharLength) {
      return 'Institution name must be at most $_maxCharLength characters.';
    }
    return null;
  }

  String? _validateFieldOfStudy(String? value) {
    // Opsional (blank=True), tetapi tetap dibatasi panjangnya.
    if ((value?.trim().length ?? 0) > _maxCharLength) {
      return 'Field of study must be at most $_maxCharLength characters.';
    }
    return null;
  }

  String? _validateGpa(String? value) {
    final text = value?.trim() ?? '';
    if (text.isEmpty) return null; // opsional
    if (!_gpaPattern.hasMatch(text)) {
      return 'Use a number like 3.75 (max two decimals, dot separator).';
    }
    final gpa = double.parse(text);
    if (gpa < 0 || gpa > 4) {
      return 'GPA must be between 0.00 and 4.00.';
    }
    return null;
  }

  String? _validateStartYear(String? _) {
    if (_startYear == null) {
      return 'Select a start year.';
    }
    return null;
  }

  String? _validateEndYear(String? _) {
    if (_endYear != null && _startYear != null && _endYear! < _startYear!) {
      return 'End year cannot be earlier than the start year.';
    }
    return null;
  }

  /// Dipanggil saat tombol Save ditekan. Semua validator dijalankan lewat
  /// [FormState.validate]; dialog ringkasan hanya muncul jika semuanya lolos.
  void _onSave() {
    FocusScope.of(context).unfocus();
    if (!_formKey.currentState!.validate()) return;

    String orDash(String value) => value.trim().isEmpty ? '-' : value.trim();

    final entries = <String, String>{
      'Institution': _institutionController.text.trim(),
      'Level': _levels[_level]!,
      'Field of Study': orDash(_fieldOfStudyController.text),
      'GPA': orDash(_gpaController.text),
      'Start Year': '$_startYear',
      'End Year': _endYear == null ? 'Ongoing' : '$_endYear',
      'Description': orDash(_descriptionController.text),
    };

    showDialog(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Education saved!'),
          content: SingleChildScrollView(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: entries.entries
                  .map((entry) => Padding(
                        padding: const EdgeInsets.symmetric(vertical: 4.0),
                        child: Text.rich(
                          TextSpan(
                            children: [
                              TextSpan(
                                text: '${entry.key}: ',
                                style: const TextStyle(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              TextSpan(text: entry.value),
                            ],
                          ),
                        ),
                      ))
                  .toList(),
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('OK'),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Add Education',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        centerTitle: true,
        backgroundColor: colorScheme.primary,
        foregroundColor: Colors.white,
      ),
      drawer: const LeftDrawer(),
      body: SafeArea(
        child: Form(
          key: _formKey,
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // === Institution Name ===
                TextFormField(
                  controller: _institutionController,
                  decoration: _decoration(
                    'Institution Name',
                    hint: 'Example: Universitas Indonesia',
                  ),
                  textInputAction: TextInputAction.next,
                  maxLength: _maxCharLength,
                  validator: _validateInstitution,
                ),
                const SizedBox(height: 12.0),

                // === Level ===
                DropdownButtonFormField<String>(
                  initialValue: _level,
                  decoration: _decoration('Education Level'),
                  items: _levels.entries
                      .map((entry) => DropdownMenuItem(
                            value: entry.key,
                            child: Text(entry.value),
                          ))
                      .toList(),
                  onChanged: (String? value) {
                    if (value != null) {
                      setState(() => _level = value);
                    }
                  },
                ),
                const SizedBox(height: 12.0),

                // === Field of Study ===
                TextFormField(
                  controller: _fieldOfStudyController,
                  decoration: _decoration(
                    'Field of Study (optional)',
                    hint: 'Example: Computer Science',
                  ),
                  textInputAction: TextInputAction.next,
                  maxLength: _maxCharLength,
                  validator: _validateFieldOfStudy,
                ),
                const SizedBox(height: 12.0),

                // === GPA ===
                TextFormField(
                  controller: _gpaController,
                  decoration: _decoration(
                    'GPA (optional)',
                    hint: 'Example: 3.75',
                  ),
                  keyboardType:
                      const TextInputType.numberWithOptions(decimal: true),
                  textInputAction: TextInputAction.next,
                  validator: _validateGpa,
                ),
                const SizedBox(height: 12.0),

                // === Start Year & End Year ===
                // Wrap membuat kedua field bersebelahan di layar lebar dan
                // turun ke baris berikutnya di layar sempit.
                LayoutBuilder(
                  builder: (context, constraints) {
                    const spacing = 12.0;
                    final isWide = constraints.maxWidth >= 420;
                    final fieldWidth = isWide
                        ? (constraints.maxWidth - spacing) / 2
                        : constraints.maxWidth;
                    return Wrap(
                      spacing: spacing,
                      runSpacing: spacing,
                      children: [
                        SizedBox(
                          width: fieldWidth,
                          child: TextFormField(
                            controller: _startYearController,
                            readOnly: true,
                            decoration: _decoration('Start Year').copyWith(
                              suffixIcon: const Icon(Icons.calendar_today),
                            ),
                            onTap: _selectStartYear,
                            validator: _validateStartYear,
                          ),
                        ),
                        SizedBox(
                          width: fieldWidth,
                          child: TextFormField(
                            controller: _endYearController,
                            readOnly: true,
                            decoration: _decoration(
                              'End Year (optional)',
                              hint: 'Leave empty if ongoing',
                            ).copyWith(
                              suffixIcon: _endYear == null
                                  ? const Icon(Icons.calendar_today)
                                  : IconButton(
                                      tooltip: 'Clear end year',
                                      icon: const Icon(Icons.clear),
                                      onPressed: _clearEndYear,
                                    ),
                            ),
                            onTap: _selectEndYear,
                            validator: _validateEndYear,
                          ),
                        ),
                      ],
                    );
                  },
                ),
                const SizedBox(height: 12.0),

                // === Description ===
                TextFormField(
                  controller: _descriptionController,
                  decoration: _decoration(
                    'Description (optional)',
                    hint: 'Achievements, organizations, thesis, etc.',
                  ).copyWith(alignLabelWithHint: true),
                  minLines: 3,
                  maxLines: 5,
                  keyboardType: TextInputType.multiline,
                ),
                const SizedBox(height: 24.0),

                // === Save Button ===
                SizedBox(
                  height: 48.0,
                  child: ElevatedButton.icon(
                    style: ElevatedButton.styleFrom(
                      backgroundColor: colorScheme.primary,
                      foregroundColor: Colors.white,
                    ),
                    onPressed: _onSave,
                    icon: const Icon(Icons.save),
                    label: const Text('Save'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
