# --- Stage 1: build ---
FROM node:20-alpine as build

# рабочая папка
WORKDIR /app

# копируем package.json и package-lock.json (или yarn.lock)
COPY package*.json ./

# устанавливаем зависимости
RUN npm install

# копируем весь фронтенд-код
COPY . .

EXPOSE 5173
# запускаем nginx
CMD ["npm", "run", "dev", "--", "--host"]