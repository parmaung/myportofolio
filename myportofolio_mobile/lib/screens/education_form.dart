import 'package:material_ui/material_ui.dart';
import 'package:myportofolio_mobile/widgets/left_drawer.dart';

/// Halaman form untuk menambahkan riwayat pendidikan.
///
/// Field mengikuti model `Education` pada aplikasi Django:
/// `institution_name`, `level`, dan `field_of_study`.
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
  String _level = 'bachelor'; // default sesuai model

  @override
  void dispose() {
    _institutionController.dispose();
    _fieldOfStudyController.dispose();
    super.dispose();
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
              ],
            ),
          ),
        ),
      ),
    );
  }
}
