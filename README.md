Muhammad Rafif Ananta Marpaung - 2506585151 (PBP B)

//////////////////////////////////////////

note:
07/09/2026 - added skill section

/////////////////////////////////////////

Reflective Question for Assignment 01:

Q1:
When you designed the HTML structure you used, did you use semantic HTML5 elements such as <section>, <article>, or <aside>? If so, how did those elements help you build the static web? If not, why did your design’s needs stay met without them?
A1:
I did use <section> in my assignment, where i used it to group things on a whole new feature and get them new headings.

Q2:
When you set up your CSS to stay responsive, what layout challenges did you encounter? How did you evaluate which elements needed to be repositioned or prioritized in size when moving from the desktop view to mobile?
A1:
As far as I know padding and grid will help alot if it comes to the flexibility between mobile and dekstop view. Padding puts on a margin so it looks more tidy and grid keep elements in position.

Q3:
The website you’ve built right now is a purely static web. What limitations did you feel while trying to present your portfolio’s information optimally? Based on those limitations, what dynamic functionality would you most want to prepare and add in the next iteration of the project?
A3:
I am learning to make my web more dynamic and fluid with more interactive elements. Such as carousels, slides, more animations for hook purposes. To the best of my knowledge im still limited to static elements where the only interaction is hover buttons, Im looking forward to learn more.

////////////////////////////////////////

Reflective Question for Assignment 03:

Q1:
Explain why we use Django’s ModelForm instead of creating HTML forms manually. Additionally, explain why we are required to add {% csrf_token %} to these forms!
A1:
Its much more practical i guess. Since hard-coding the HTML is much more of a repetitive process, and the data from Django is much more validated.

Q2:
In Tutorial 03, we discussed JSON and XML data formats. Why is JSON preferred in modern web application development compared to XML?
A1:
I need some google searchfor this and actually comparing it to my knowledge. And as far as I understand, JSON is fairly much simpler to use.

Q3:
Explain the flow that occurs when you use a view function to return your portfolio data in JSON format. Why do we need to perform the serialization process on Django models before returning the data?
A3:
The client sends a request to views.py, and the database returns the response. (still trying to understand to be honest)

////////////////////////////////////////

### Assignment 8

Feature added: an **Add Education** form page (`myportofolio_mobile/lib/screens/education_form.dart`) that follows the Django `Education` model (institution name, level, field of study, GPA, start year, end year, description). It can be opened from the **Add Education** action card on the home screen and from the **Add Education** option in the drawer.

How to run (inside `myportofolio_mobile/`):

```bash
flutter create .      # only once, generates the platform folders
flutter pub get
flutter analyze
flutter run -d chrome
```

1. `Navigator.push()` puts a new route on top of the navigation stack, so the previous page is still underneath and can be returned to. `Navigator.pushReplacement()` also opens a new route, but it removes the current route first, so pressing Back will not go to the page that was replaced. `Navigator.pop()` removes the top route and goes back to the page below it (it is also used to close dialogs). The **Add Education** action card uses `Navigator.push()`, so the form sits on top of the home screen and the system Back button (or the AppBar back arrow) pops it and goes back to home. The drawer options for the forms use `pushReplacement()` so moving between pages from the drawer does not keep piling up routes. For **Home**, the drawer uses `Navigator.pushAndRemoveUntil(..., (route) => false)`, which opens a fresh `MyHomePage` and removes every route underneath it. That way home always becomes the only page on the stack, even if the form was opened with `push()` before (with a plain `pushReplacement()` there would be two home pages in the stack).

2. Every page uses the same skeleton: a `Scaffold` as the base, an `AppBar` on top for the title, a `drawer:` slot that always holds the same `LeftDrawer` widget, and a `body` for the content. Because `LeftDrawer` lives in `lib/widgets/` and is reused on the home, Add Project, and Add Education pages, the menu items and their order are always the same, and adding a new menu only needs one change. The theme color is also shared: `main.dart` sets `ColorScheme.fromSeed(seedColor: Colors.indigo)`, and both the home page and the Add Education page use `Theme.of(context).colorScheme.primary` as the `AppBar` background (and the Education Save button uses it too), so the indigo color is the same on more than one page. The drawer header is indigo as well, and the action cards use the orange `secondary` color.

3. The form is one vertical column because it is the easiest to read and fill on a phone: one field per row, label on top of each input, and the Save button at the end. The body is `SafeArea` -> `Form` -> `SingleChildScrollView` -> `Column`. `SafeArea` keeps the content away from the notch and system bars. `SingleChildScrollView` is the most important part: when the screen is short or the keyboard is open (the `Scaffold` shrinks the body when the keyboard appears), the column can be scrolled, so no field and not the Save button get cut off or cause an overflow error. `SizedBox(height: ...)` gives consistent gaps between fields so they don't stick together, and the padding keeps them away from the screen edges. The start year and end year fields are inside a `LayoutBuilder` + `Wrap`: on a wide screen (like Chrome) they are side by side, and on a narrow screen each takes the full width and moves to its own line. I also made the home screen scrollable since adding a fourth action card could overflow on small phones.

4. `GlobalKey<FormState>` is the key attached to the `Form` widget, so I can reach the form's state from outside the fields with `_formKey.currentState`. Each `TextFormField` has a `validator` function that receives the value and returns an error message string when the value is wrong, or `null` when it is fine. When Save is pressed, `_formKey.currentState!.validate()` runs every validator in the form at once, shows the error text under each invalid field, and returns `true` only if all of them returned `null`. Only then the `AlertDialog` with the summary is shown. Example of a rejected value: GPA `4.5` (or `3,75`, or `3.756`). The GPA field uses `TextInputType.numberWithOptions(decimal: true)`, but the keyboard type is only a hint: on Chrome/desktop there is no on-screen keyboard at all, users can paste any text, and even the numeric keyboard still allows numbers that are out of range or have too many decimals. So the validator checks the format (`^\d(\.\d{1,2})?$`, same as `DecimalField(max_digits=4, decimal_places=2)`) and the range 0.00-4.00. Another example is an institution name that only contains spaces: the field "has text", but `value.trim().isEmpty` rejects it. The year picker also can't stop the user from picking an end year earlier than the start year, so the end year validator checks that order.

////////////////////////////////////////
