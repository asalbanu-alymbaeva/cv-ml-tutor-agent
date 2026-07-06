from tutor.services import get_tutor_response

result = get_tutor_response("CNN qanday ishlaydi?")

print("=== REJA ===")
print(result["plan"])
print("\n=== TUSHUNTIRISH (draft) ===")
print(result["draft"])
print("\n=== YAKUNIY (final) ===")
print(result["final"])