with open("log.txt","a") as register:
  date = "07/08/2026"
  heading = f"\nLogged on {date}"
  register.write(heading)
  people = 4
  # 0 1 2 3
  for i in range(people):
    name = input("Enter the name: ")
    flat_no = int(input("Enter flat no: "))

    data = f"\n{i+1}){name} - {flat_no}"
    register.write(data)

  footer = f"\nLog completed for {date}"
  register.write(footer)  